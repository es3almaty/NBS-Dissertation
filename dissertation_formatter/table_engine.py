from __future__ import annotations

import math
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from .models import TableAssessment, TableRisk, Finding, Severity, Action

# Captions in real student documents sometimes contain harmless OCR/typing artefacts
# such as "Таблицао" or use any of several dash characters. Keep matching tolerant,
# but only at the beginning of a paragraph so ordinary prose references are not captions.
CAPTION_RE = re.compile(r"^(?:таблица(?:о)?|table|кесте)\s*(\d+)\b\s*[-–—:.]?\s*(.*)$", re.I)


def normalize_caption_text(text: str) -> str:
    """Normalize only leading caption artefacts; never rewrite document content."""
    s = (text or "").strip()
    s = re.sub(r"^(таблица)о\s+", r"\1 ", s, flags=re.I)
    # A stray Cyrillic 'о' is occasionally inserted immediately after the separator.
    s = re.sub(r"^(таблица|table|кесте)\s*(\d+)\s*([-–—:.])\s*о\s+", r"\1 \2 \3 ", s, flags=re.I)
    return s


def _grid_widths(tbl) -> list[int]:
    grid = tbl._tbl.tblGrid
    widths = []
    if grid is not None:
        for col in grid.gridCol_lst:
            w = col.get(qn("w:w"))
            if w and w.isdigit():
                widths.append(int(w))
    return widths


def _has_merge(tbl) -> bool:
    xml = tbl._tbl.xml
    return "w:gridSpan" in xml or "w:vMerge" in xml


def _caption_before(doc, table_index: int) -> tuple[str | None, int | None]:
    """Associate a Word table with the nearest preceding caption.

    Real documents commonly place one or more blank paragraphs between a caption and
    the table, and long captions may wrap into a second Word paragraph. The old engine
    only looked at the immediately preceding paragraph, missing most real captions.
    This routine looks back a small bounded window and joins short continuation lines.
    """
    body = doc.element.body
    seen_tables = -1
    history: list[str] = []
    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            texts = child.xpath(".//w:t/text()")
            history.append("".join(texts).strip())
            if len(history) > 8:
                history = history[-8:]
        elif child.tag.endswith("}tbl"):
            seen_tables += 1
            if seen_tables != table_index:
                # A caption cannot sensibly jump over a previous table.
                history = []
                continue
            # Search from nearest to farthest for a caption starter.
            for k in range(len(history) - 1, -1, -1):
                base = normalize_caption_text(history[k])
                m = CAPTION_RE.match(base)
                if not m:
                    continue
                # At most two non-empty continuation paragraphs are allowed between
                # the caption start and the table. This catches wrapped captions but
                # avoids swallowing ordinary prose.
                continuations = [x.strip() for x in history[k + 1:] if x.strip()]
                if len(continuations) > 2:
                    continue
                caption = " ".join([base] + continuations).strip()
                mm = CAPTION_RE.match(normalize_caption_text(caption))
                return (caption, int(mm.group(1))) if mm else (None, None)
            return None, None
    return None, None


def _severe_narrow_grid(widths: list[int], texts: list[str]) -> tuple[bool, str | None]:
    """Detect genuinely crushed tables without penalizing narrow index columns.

    A 400-500 twip first column is common for '№'. v0.2 previously treated that as a
    broken table whenever *any* other cell contained long text. A table is now flagged
    from grid width alone only when narrowness is systemic across multiple columns.
    """
    if not widths:
        return False, None
    narrow = [w for w in widths if w < 500]
    very_narrow = [w for w in widths if w < 300]
    max_text = max((len(re.sub(r"\s+", "", x or "")) for x in texts), default=0)
    systemic = len(narrow) >= 2 and len(narrow) / len(widths) >= 0.40
    extremely_crushed = len(very_narrow) >= 2
    if max_text > 20 and (systemic or extremely_crushed):
        return True, f"systemically narrow table grid detected (minimum {min(widths)} twips; {len(narrow)}/{len(widths)} columns <500 twips)"
    return False, None


def analyze_tables(path: str | Path) -> tuple[list[TableAssessment], list[Finding]]:
    doc = Document(path)
    assessments = []
    findings = []
    nums = []
    for i, tbl in enumerate(doc.tables):
        caption, num = _caption_before(doc, i)
        if num is not None:
            nums.append(num)
        rows = len(tbl.rows)
        cols = max((len(r.cells) for r in tbl.rows), default=0)
        widths = _grid_widths(tbl)
        reasons = []
        texts = [c.text for r in tbl.rows for c in r.cells]
        one_char_lines = sum(
            1
            for x in texts
            if len([ln for ln in x.splitlines() if ln.strip()]) >= 5
            and sum(len(ln.strip()) <= 2 for ln in x.splitlines()) >= 4
        )
        severe_narrow, narrow_reason = _severe_narrow_grid(widths, texts)
        if one_char_lines:
            reasons.append("cell text is fragmented into many one- or two-character lines")
        if severe_narrow and narrow_reason:
            reasons.append(narrow_reason)
        if one_char_lines or severe_narrow:
            risk = TableRisk.BROKEN_REQUIRES_REVIEW
        elif _has_merge(tbl) or cols > 6 or rows > 40:
            risk = TableRisk.COMPLEX_SAFE_TO_PRESERVE
            if _has_merge(tbl):
                reasons.append("merged cells")
            if cols > 6:
                reasons.append(f"{cols} columns")
            if rows > 40:
                reasons.append(f"{rows} rows")
        else:
            risk = TableRisk.SIMPLE_SAFE
        assessments.append(TableAssessment(i + 1, caption, num, risk, reasons, rows, cols))
        if risk == TableRisk.BROKEN_REQUIRES_REVIEW:
            findings.append(
                Finding(
                    "BROKEN_TABLE",
                    f"Table {num or i + 1} requires review",
                    "The table appears structurally/readability-broken and will be preserved rather than aggressively reformatted. "
                    + "; ".join(reasons),
                    Severity.MAJOR,
                    Action.MANUAL_REVIEW,
                    location=f"table_index={i + 1}",
                )
            )
    # Duplicates and gaps based only on explicit captions.
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    if duplicates:
        findings.append(
            Finding(
                "DUPLICATE_TABLE_NUMBERS",
                "Duplicate table numbers",
                "Duplicate table numbers detected: " + ", ".join(map(str, duplicates)),
                Severity.MAJOR,
                Action.FLAG,
                evidence={"numbers": duplicates},
            )
        )
    if nums:
        uniq = sorted(set(nums))
        gaps = [n for n in range(min(uniq), max(uniq) + 1) if n not in uniq]
        if gaps:
            findings.append(
                Finding(
                    "TABLE_NUMBERING_GAPS",
                    "Table numbering gaps",
                    "Missing table numbers in detected caption sequence: " + ", ".join(map(str, gaps)),
                    Severity.MINOR,
                    Action.FLAG,
                    evidence={"numbers": gaps},
                )
            )
    return assessments, findings
