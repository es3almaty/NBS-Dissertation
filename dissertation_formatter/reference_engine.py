from __future__ import annotations

import re
from pathlib import Path
from docx import Document
from .models import ReferenceAssessment, CitationSystem, Finding, Severity, Action
from .structure_detector import norm, HEADING_PATTERNS

NUMERIC_RE = re.compile(r"\[(\d+(?:\s*[,;\-]\s*\d+)*)(?:[^\]]*)\]")
AUTHOR_DATE_RE = re.compile(r"\(([A-ZА-ЯӘҒҚҢӨҰҮҺЁ][A-Za-zА-Яа-яӘәҒғҚқҢңӨөҰұҮүҺһЁё'’\-]+(?:\s+(?:&|and|и)\s+[A-ZА-ЯӘҒҚҢӨҰҮҺЁ][^,;()]+)?),\s*(20\d{2}|19\d{2}|n\.d\.|н\.д\.)[a-zа-я]?\)")


def _ref_heading_index(paras: list[str]) -> int | None:
    for i,p in enumerate(paras):
        n=norm(p)
        if any(re.match(rx,n,re.I) for rx in HEADING_PATTERNS["references"]):
            return i
    return None


def analyze_references(path: str | Path, footnotes_present: bool=False) -> tuple[ReferenceAssessment, list[Finding]]:
    doc=Document(path)
    paras=[p.text.strip() for p in doc.paragraphs]
    text="\n".join(paras)
    numeric=[]
    for m in NUMERIC_RE.finditer(text):
        nums=re.findall(r"\d+",m.group(1))
        numeric.extend(int(x) for x in nums)
    author=[f"{m.group(1)}, {m.group(2)}" for m in AUTHOR_DATE_RE.finditer(text)]
    systems=sum([bool(numeric),bool(author),footnotes_present])
    if systems > 1:
        sys=CitationSystem.MIXED
    elif numeric:
        sys=CitationSystem.NUMERIC
    elif author:
        sys=CitationSystem.APA_AUTHOR_DATE
    elif footnotes_present:
        sys=CitationSystem.FOOTNOTE
    else:
        sys=CitationSystem.NO_DETECTABLE_SYSTEM
    rhi=_ref_heading_index(paras)
    refs_present=rhi is not None
    unmatched=[]; uncited=[]; dupes=[]
    findings=[]
    entries=[]
    if refs_present:
        entries=[]
        for p in paras[rhi+1:]:
            if not p.strip():
                continue
            if re.match(r"^(?:таблица|table|кесте|рисунок|рис\.?|figure|сурет|приложение|appendix|қосымша)\s+\d+", p.strip(), re.I):
                break
            entries.append(p)
        normalized=[norm(e) for e in entries]
        seen=set()
        for raw,n in zip(entries,normalized):
            if n in seen:
                dupes.append(raw)
            seen.add(n)
        # Conservative author-date matching using surname+year.
        if author:
            entry_text="\n".join(entries).lower()
            for c in sorted(set(author)):
                surname,year=[x.strip() for x in c.rsplit(",",1)]
                if surname.lower().split()[0] not in entry_text or year.lower() not in entry_text:
                    unmatched.append(c)
        # Numeric bibliographies often have explicit [n] or n. labels; flag citations whose labels absent.
        if numeric:
            labels=set()
            for e in entries:
                m=re.match(r"^\s*\[?(\d+)\]?[.)]?\s+",e)
                if m: labels.add(int(m.group(1)))
            if labels:
                unmatched.extend(str(n) for n in sorted(set(numeric)-labels))
    elif numeric:
        findings.append(Finding(
            "NUMERIC_CITATIONS_NO_BIBLIOGRAPHY", "Numeric citations detected but References is missing",
            "Numeric in-text citations were detected, but no References section was found. The bibliography must not be reconstructed or inferred. Detected citation numbers: " + ", ".join(map(str,sorted(set(numeric)))),
            Severity.CRITICAL, Action.BLOCK_FORMATTING,
            evidence={"numeric_citations": sorted(set(numeric))},
        ))
    if unmatched:
        findings.append(Finding("UNMATCHED_CITATIONS", "Citations without a matched bibliography entry", "The following in-text citations could not be conservatively matched to supplied bibliography entries: " + ", ".join(unmatched), Severity.MAJOR, Action.FLAG))
    if dupes:
        findings.append(Finding("DUPLICATE_REFERENCE_ENTRIES", "Possible duplicate bibliography entries", f"Detected {len(dupes)} duplicate normalized reference entries.", Severity.MINOR, Action.FLAG, evidence={"entries":dupes}))
    return ReferenceAssessment(sys,refs_present,sorted(set(numeric)),sorted(set(author)),unmatched,uncited,dupes),findings
