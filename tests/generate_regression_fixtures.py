from pathlib import Path
from fixtures import *

out=Path(__file__).resolve().parents[1]/'synthetic_fixtures';out.mkdir(exist_ok=True)
scenarios={
'01_fully_compliant':{},
'02_two_missing':{'contents':False,'summary':False},
'03_three_missing':{'contents':False,'summary':False,'annotations':False},
'04_unmatched_citation':{'citation':'(Jones, 2025)'},
'05_numeric_no_bibliography':{'references':False,'citation':'[1] [4, p. 45] [25]'},
'10_contents_mismatch':{'contents_mismatch':True},
}
for name,kwargs in scenarios.items():build_base(out/f'{name}.docx',**kwargs)
p=build_base(out/'06_duplicate_tables.docx');add_duplicate_table_numbers(p)
p=build_base(out/'07_broken_table.docx');add_broken_table(p)
p=build_base(out/'08_duplicate_page_fields.docx');add_duplicate_page_fields(p)
p=build_base(out/'09_automatic_numbering.docx');add_automatic_heading_numbering(p)
p=build_base(out/'11_numeric_inconsistency.docx');add_numeric_inconsistency(p)
p=build_base(out/'12_appendix_mismatch.docx');add_appendix_reference_without_appendix(p)
print(out)
