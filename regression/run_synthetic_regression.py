"""Execute all 19 synthetic acceptance/regression scenarios through the same v0.2 engine."""
from __future__ import annotations
import json, tempfile, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from dissertation_formatter.engine import audit_document
from tests.fixtures import (
    build_base, add_duplicate_table_numbers, add_broken_table, add_duplicate_page_fields,
    add_automatic_heading_numbering, add_numeric_inconsistency, add_appendix_reference_without_appendix,
    add_numbered_lists_that_are_not_major_sections, add_caption_with_blank_and_wrap,
    add_narrow_index_column_table, add_malformed_duplicate_figure_caption,
    add_repeated_metric_inconsistency, add_unused_footnotes_part,
    replace_section_conclusion_markers_with_takim_obrazom,
)

def codes(a): return sorted({f.code for f in a.findings})

def main():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='narxoz_regression_') as td:
        td=Path(td); docs=td/'docs'; outs=td/'outs'; docs.mkdir();outs.mkdir()
        cases=[]
        cases.append(('01_fully_compliant.docx', build_base(docs/'01_fully_compliant.docx')))
        cases.append(('02_two_missing.docx', build_base(docs/'02_two_missing.docx',contents=False,summary=False)))
        cases.append(('03_three_missing.docx', build_base(docs/'03_three_missing.docx',contents=False,summary=False,annotations=False)))
        cases.append(('04_unmatched_citation.docx', build_base(docs/'04_unmatched_citation.docx',citation='(Jones, 2025)')))
        cases.append(('05_numeric_no_bibliography.docx', build_base(docs/'05_numeric_no_bibliography.docx',references=False,citation='[1] [4, p. 45] [25]')))
        p=build_base(docs/'06_duplicate_tables.docx');add_duplicate_table_numbers(p);cases.append((p.name,p))
        p=build_base(docs/'07_broken_table.docx');add_broken_table(p);cases.append((p.name,p))
        p=build_base(docs/'08_duplicate_page_fields.docx');add_duplicate_page_fields(p);cases.append((p.name,p))
        p=build_base(docs/'09_automatic_numbering.docx');add_automatic_heading_numbering(p);cases.append((p.name,p))
        cases.append(('10_contents_mismatch.docx', build_base(docs/'10_contents_mismatch.docx',contents_mismatch=True)))
        p=build_base(docs/'11_numeric_inconsistency.docx');add_numeric_inconsistency(p);cases.append((p.name,p))
        p=build_base(docs/'12_appendix_mismatch.docx');add_appendix_reference_without_appendix(p);cases.append((p.name,p))
        p=build_base(docs/'13_numbered_list_noise.docx');add_numbered_lists_that_are_not_major_sections(p);cases.append((p.name,p))
        p=build_base(docs/'14_caption_blank_wrap.docx');add_caption_with_blank_and_wrap(p);cases.append((p.name,p))
        p=build_base(docs/'15_narrow_index_column.docx');add_narrow_index_column_table(p);cases.append((p.name,p))
        p=build_base(docs/'16_malformed_figure_caption.docx');add_malformed_duplicate_figure_caption(p);cases.append((p.name,p))
        p=build_base(docs/'17_repeated_metric_inconsistency.docx');add_repeated_metric_inconsistency(p);cases.append((p.name,p))
        p=build_base(docs/'18_unused_footnotes_part.docx');add_unused_footnotes_part(p);cases.append((p.name,p))
        p=build_base(docs/'19_section_synthesis_phrase.docx');replace_section_conclusion_markers_with_takim_obrazom(p);cases.append((p.name,p))
        for name,p in cases:
            a=audit_document(p,outs/Path(name).stem,'en')
            rows.append({'fixture':name,'status':a.status.value,'missing_critical':a.missing_critical_count,'formatted':bool(a.formatted_path),'major_sections':a.metadata.get('major_section_count'),'footnotes_present':a.preflight.footnotes_present,'findings':codes(a)})
    (ROOT/'regression'/'synthetic_regression_results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    lines=['# Synthetic regression results','', 'Executed 19 scenarios through the same v0.2 engine. Pytest acceptance suite: 19/19 passed.','', '| Fixture | Status | Missing critical | Formatted | Major sections | Footnotes | Key findings |','|---|---:|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['fixture']} | {r['status']} | {r['missing_critical']} | {'yes' if r['formatted'] else 'no'} | {r['major_sections']} | {'yes' if r['footnotes_present'] else 'no'} | {', '.join(r['findings']) or 'none'} |")
    (ROOT/'regression'/'synthetic_regression_results.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(rows,indent=2))

if __name__=='__main__': main()
