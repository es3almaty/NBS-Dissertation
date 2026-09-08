from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
import re
import zipfile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W, "r": R, "pr": PKG_REL}


class ContentIntegrityError(RuntimeError):
    """Raised when formatting changes student content rather than presentation only."""


@dataclass
class IntegrityResult:
    passed: bool
    checks: dict[str, bool] = field(default_factory=dict)
    details: dict[str, object] = field(default_factory=dict)

    @property
    def failures(self) -> list[str]:
        return [name for name, ok in self.checks.items() if not ok]

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "checks": dict(self.checks),
            "failures": self.failures,
            "details": dict(self.details),
        }


def _is_field_element(el) -> bool:
    return el.tag in {f"{{{W}}}fldChar", f"{{{W}}}instrText", f"{{{W}}}fldSimple"}


def _semantic_tokens(xml_bytes: bytes, *, ignore_fields: bool = False) -> tuple[str, ...]:
    """Return a formatting-insensitive token stream while preserving document structure.

    Run/paragraph properties are deliberately ignored. Paragraph, table, row, cell, text,
    tab and break boundaries are retained. In headers/footers, field contents can be ignored
    so adding/deduplicating PAGE fields does not look like a student-content change.
    """
    root = etree.fromstring(xml_bytes)
    tokens: list[str] = []
    field_depth = 0

    def walk(el):
        nonlocal field_depth
        local = etree.QName(el).localname
        ns = etree.QName(el).namespace

        if ignore_fields and ns == W and local == "fldSimple":
            return
        if ignore_fields and ns == W and local == "fldChar":
            typ = el.get(f"{{{W}}}fldCharType", "")
            if typ == "begin":
                field_depth += 1
            elif typ == "end" and field_depth:
                field_depth -= 1
            return
        if ignore_fields and field_depth:
            # Still traverse only so a nested/end field marker can close the field.
            for child in el:
                walk(child)
            return

        if ns == W:
            if local == "p": tokens.append("<P>")
            elif local == "tbl": tokens.append("<TBL>")
            elif local == "tr": tokens.append("<TR>")
            elif local == "tc": tokens.append("<TC>")
            elif local in {"t", "delText", "instrText"}:
                tokens.append("TXT:" + (el.text or ""))
            elif local == "tab": tokens.append("<TAB>")
            elif local == "br": tokens.append("<BR:" + (el.get(f"{{{W}}}type") or "textWrapping") + ">")
            elif local == "cr": tokens.append("<CR>")
            elif local == "noBreakHyphen": tokens.append("<NBH>")
            elif local == "softHyphen": tokens.append("<SHY>")
            elif local == "fldChar" and not ignore_fields:
                tokens.append("<FLD:" + (el.get(f"{{{W}}}fldCharType") or "") + ">")
        for child in el:
            walk(child)
        if ns == W:
            if local == "p": tokens.append("</P>")
            elif local == "tbl": tokens.append("</TBL>")
            elif local == "tr": tokens.append("</TR>")
            elif local == "tc": tokens.append("</TC>")

    walk(root)
    return tuple(tokens)


def _xml_part_signature(zf: zipfile.ZipFile, name: str, *, ignore_fields: bool = False):
    if name not in zf.namelist():
        return None
    return _semantic_tokens(zf.read(name), ignore_fields=ignore_fields)


def _header_footer_signatures(zf: zipfile.ZipFile, prefix: str) -> tuple[tuple[str, ...], ...]:
    sigs=[]
    rx=re.compile(rf"^word/{prefix}\d+\.xml$")
    for name in zf.namelist():
        if rx.match(name):
            sig=_semantic_tokens(zf.read(name), ignore_fields=True)
            # A formatter-created header containing only a PAGE field is semantically empty.
            meaningful=tuple(t for t in sig if t not in {"<P>","</P>"})
            if meaningful:
                sigs.append(sig)
    return tuple(sorted(sigs))


def _payload_hashes(zf: zipfile.ZipFile, prefixes: tuple[str, ...]) -> tuple[str, ...]:
    vals=[]
    for name in zf.namelist():
        if any(name.startswith(p) for p in prefixes) and not name.endswith("/") and "/_rels/" not in name:
            vals.append(sha256(zf.read(name)).hexdigest())
    return tuple(sorted(vals))


def _hyperlinks(zf: zipfile.ZipFile) -> tuple[str, ...]:
    targets=[]
    for name in zf.namelist():
        if not name.endswith(".rels") or not name.startswith("word/"):
            continue
        try:
            root=etree.fromstring(zf.read(name))
        except etree.XMLSyntaxError:
            continue
        for rel in root.xpath('.//*[local-name()="Relationship"]'):
            typ=rel.get("Type", "")
            if typ.endswith("/hyperlink"):
                targets.append(rel.get("Target", ""))
    return tuple(sorted(targets))


def _package_snapshot(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path, "r") as zf:
        snap={
            "document": _xml_part_signature(zf,"word/document.xml"),
            "footnotes": _xml_part_signature(zf,"word/footnotes.xml") or (),
            "endnotes": _xml_part_signature(zf,"word/endnotes.xml") or (),
            "comments": _xml_part_signature(zf,"word/comments.xml") or (),
            "headers": _header_footer_signatures(zf,"header"),
            "footers": _header_footer_signatures(zf,"footer"),
            "hyperlinks": _hyperlinks(zf),
            "media": _payload_hashes(zf,("word/media/",)),
            "embedded_content": _payload_hashes(zf,("word/embeddings/","word/charts/","word/diagrams/","word/activeX/","customXml/")),
        }
    return snap


def verify_content_integrity(original_path: str|Path, formatted_path: str|Path) -> IntegrityResult:
    original=Path(original_path); formatted=Path(formatted_path)
    a=_package_snapshot(original); b=_package_snapshot(formatted)
    checks={name:(a[name]==b[name]) for name in a}
    details={
        "document_token_count_original": len(a["document"] or ()),
        "document_token_count_formatted": len(b["document"] or ()),
        "media_count_original": len(a["media"]),
        "media_count_formatted": len(b["media"]),
        "hyperlink_count_original": len(a["hyperlinks"]),
        "hyperlink_count_formatted": len(b["hyperlinks"]),
        "embedded_content_count_original": len(a["embedded_content"]),
        "embedded_content_count_formatted": len(b["embedded_content"]),
    }
    return IntegrityResult(all(checks.values()),checks,details)


def assert_content_integrity(original_path: str|Path, formatted_path: str|Path) -> IntegrityResult:
    result=verify_content_integrity(original_path,formatted_path)
    if not result.passed:
        raise ContentIntegrityError(
            "Post-format content integrity check failed: " + ", ".join(result.failures)
        )
    return result


def has_dynamic_toc(path: str|Path) -> bool:
    """Return True when the DOCX contains a Word TOC field rather than only typed page numbers."""
    path=Path(path)
    with zipfile.ZipFile(path,"r") as zf:
        if "word/document.xml" not in zf.namelist(): return False
        root=etree.fromstring(zf.read("word/document.xml"))
        instr=[]
        instr.extend(root.xpath('.//w:instrText/text()',namespaces=NS))
        instr.extend(root.xpath('.//w:fldSimple/@w:instr',namespaces=NS))
    return any(re.search(r"(?:^|\s)TOC(?:\s|$)",x or "",re.I) for x in instr)
