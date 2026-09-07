from __future__ import annotations

import re
import zipfile
from collections import defaultdict
from pathlib import Path
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W_NS, "m": M_NS, "r": R_NS}


def qn(local: str) -> str:
    return f"{{{W_NS}}}{local}"


def read_zip_xml(path: str | Path, part: str):
    with zipfile.ZipFile(path) as zf:
        try:
            return etree.fromstring(zf.read(part))
        except KeyError:
            return None


def zip_parts(path: str | Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        return zf.namelist()


def text_of_paragraph_el(p) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()


def parse_numbering(path: str | Path) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    """Return numId -> ilvl -> numFmt, and styleId -> numId maps."""
    numbering = read_zip_xml(path, "word/numbering.xml")
    num_map: dict[str, dict[str, str]] = {}
    abstract_map: dict[str, dict[str, str]] = {}
    if numbering is not None:
        for absn in numbering.xpath(".//w:abstractNum", namespaces=NS):
            aid = absn.get(qn("abstractNumId"))
            levels = {}
            for lvl in absn.xpath("./w:lvl", namespaces=NS):
                ilvl = lvl.get(qn("ilvl"), "0")
                fmt = lvl.find("w:numFmt", NS)
                levels[ilvl] = fmt.get(qn("val"), "") if fmt is not None else ""
            abstract_map[aid] = levels
        for n in numbering.xpath(".//w:num", namespaces=NS):
            nid = n.get(qn("numId"))
            aid_el = n.find("w:abstractNumId", NS)
            aid = aid_el.get(qn("val")) if aid_el is not None else None
            num_map[nid] = abstract_map.get(aid, {})
    styles = read_zip_xml(path, "word/styles.xml")
    style_num: dict[str, str] = {}
    if styles is not None:
        for style in styles.xpath(".//w:style", namespaces=NS):
            sid = style.get(qn("styleId"))
            numid_el = style.find("w:pPr/w:numPr/w:numId", NS)
            if sid and numid_el is not None:
                style_num[sid] = numid_el.get(qn("val"))
    return num_map, style_num


def paragraph_numbering_info(path: str | Path) -> list[dict]:
    doc = read_zip_xml(path, "word/document.xml")
    if doc is None:
        return []
    num_map, style_num = parse_numbering(path)
    out = []
    paras = doc.xpath(".//w:body/w:p", namespaces=NS)
    for idx, p in enumerate(paras):
        numid_el = p.find("w:pPr/w:numPr/w:numId", NS)
        ilvl_el = p.find("w:pPr/w:numPr/w:ilvl", NS)
        style_el = p.find("w:pPr/w:pStyle", NS)
        style = style_el.get(qn("val")) if style_el is not None else None
        numid = numid_el.get(qn("val")) if numid_el is not None else style_num.get(style or "")
        if numid is None:
            continue
        ilvl = ilvl_el.get(qn("val"), "0") if ilvl_el is not None else "0"
        out.append({
            "paragraph_index": idx,
            "text": text_of_paragraph_el(p),
            "style": style,
            "numId": numid,
            "ilvl": ilvl,
            "numFmt": num_map.get(numid, {}).get(ilvl, ""),
        })
    return out


def field_instructions(root) -> list[str]:
    if root is None:
        return []
    ins = []
    for t in root.xpath(".//w:instrText/text()", namespaces=NS):
        if t and t.strip():
            ins.append(t.strip())
    for fs in root.xpath(".//w:fldSimple", namespaces=NS):
        val = fs.get(qn("instr"))
        if val:
            ins.append(val.strip())
    return ins


def count_page_fields_by_part(path: str | Path) -> dict[str, int]:
    parts = zip_parts(path)
    candidate = [p for p in parts if p == "word/document.xml" or re.match(r"word/(header|footer)\d+\.xml$", p)]
    counts = {}
    for part in candidate:
        root = read_zip_xml(path, part)
        counts[part] = sum(1 for i in field_instructions(root) if re.search(r"\bPAGE\b", i, re.I))
    return counts


def remove_extra_page_fields_from_xml(xml_bytes: bytes, keep: int = 1) -> tuple[bytes, int]:
    """Conservatively remove fldSimple PAGE nodes and complex PAGE field runs after first."""
    root = etree.fromstring(xml_bytes)
    removed = 0
    seen = 0
    # fldSimple is easy and safe.
    for fs in list(root.xpath(".//w:fldSimple", namespaces=NS)):
        instr = fs.get(qn("instr"), "")
        if re.search(r"\bPAGE\b", instr, re.I):
            seen += 1
            if seen > keep:
                parent = fs.getparent(); parent.remove(fs); removed += 1
    # Complex fields: identify runs from begin through end in the same paragraph.
    for p in root.xpath(".//w:p", namespaces=NS):
        runs = p.findall("w:r", NS)
        i = 0
        while i < len(runs):
            begin = runs[i].find("w:fldChar", NS)
            if begin is None or begin.get(qn("fldCharType")) != "begin":
                i += 1; continue
            j = i + 1; instr = []
            while j < len(runs):
                instr.extend(runs[j].xpath(".//w:instrText/text()", namespaces=NS))
                end = runs[j].find("w:fldChar", NS)
                if end is not None and end.get(qn("fldCharType")) == "end":
                    break
                j += 1
            if j < len(runs) and re.search(r"\bPAGE\b", " ".join(instr), re.I):
                seen += 1
                if seen > keep:
                    for r in runs[i:j+1]:
                        if r.getparent() is p:
                            p.remove(r)
                    removed += 1
            i = max(j + 1, i + 1)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"), removed
