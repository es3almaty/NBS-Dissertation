from __future__ import annotations
import zipfile
from pathlib import Path
import pytest
from dissertation_formatter.engine import audit_document
from dissertation_formatter.models import SubmissionStatus, TableRisk, CitationSystem
from dissertation_formatter.ooxml_utils import count_page_fields_by_part
from .fixtures import *


def codes(a):return {f.code for f in a.findings}


def test_01_fully_compliant_ready(tmp_path):
    p=build_base(tmp_path/'full.docx')
    a=audit_document(p,tmp_path/'out','en')
    assert a.status==SubmissionStatus.READY
    assert a.missing_critical_count==0
    assert Path(a.formatted_path).exists() and Path(a.report_path).exists()


def test_02_exactly_two_missing_is_conditional_and_formats(tmp_path):
    p=build_base(tmp_path/'two_missing.docx',contents=False,summary=False)
    a=audit_document(p,tmp_path/'out','en')
    assert a.missing_critical_count==2
    assert a.status==SubmissionStatus.CONDITIONAL
    assert a.formatted_path and Path(a.formatted_path).exists()


def test_03_three_missing_is_resubmit_and_no_format(tmp_path):
    p=build_base(tmp_path/'three_missing.docx',contents=False,summary=False,annotations=False)
    a=audit_document(p,tmp_path/'out','en')
    assert a.missing_critical_count==3
    assert a.status==SubmissionStatus.RESUBMIT
    assert a.formatted_path is None
    assert 'NONCOMPLIANCE_REPORT' in a.report_path


def test_04_bibliography_present_unmatched_citation(tmp_path):
    p=build_base(tmp_path/'unmatched.docx',citation='(Jones, 2025)')
    a=audit_document(p,tmp_path/'out','en')
    assert a.references.references_present
    assert 'UNMATCHED_CITATIONS' in codes(a)


def test_05_numeric_citations_no_bibliography(tmp_path):
    p=build_base(tmp_path/'numeric.docx',references=False,citation='[1] and [4, p. 45] and [25]')
    a=audit_document(p,tmp_path/'out','en')
    assert a.references.system==CitationSystem.NUMERIC
    assert a.references.numeric_citations==[1,4,25]
    assert 'NUMERIC_CITATIONS_NO_BIBLIOGRAPHY' in codes(a)


def test_06_duplicate_table_numbering(tmp_path):
    p=build_base(tmp_path/'duptable.docx');add_duplicate_table_numbers(p)
    a=audit_document(p,tmp_path/'out','en')
    assert 'DUPLICATE_TABLE_NUMBERS' in codes(a)


def test_07_broken_table(tmp_path):
    p=build_base(tmp_path/'broken.docx');add_broken_table(p)
    a=audit_document(p,tmp_path/'out','en')
    assert any(t.risk==TableRisk.BROKEN_REQUIRES_REVIEW for t in a.tables)
    assert 'BROKEN_TABLE' in codes(a)


def test_08_duplicate_page_fields_removed_on_format(tmp_path):
    p=build_base(tmp_path/'pages.docx');add_duplicate_page_fields(p)
    a=audit_document(p,tmp_path/'out','en')
    assert a.preflight.duplicate_page_fields
    assert 'DUPLICATE_PAGE_FIELDS' in codes(a)
    counts=count_page_fields_by_part(a.formatted_path)
    assert all(v<=1 for k,v in counts.items() if 'header' in k or 'footer' in k)


def test_09_automatic_heading_numbering_detected(tmp_path):
    p=build_base(tmp_path/'autonum.docx');add_automatic_heading_numbering(p)
    a=audit_document(p,tmp_path/'out','en')
    assert a.preflight.automatic_numbering_paragraphs
    assert 'AUTOMATIC_WORD_NUMBERING_DETECTED' in codes(a)
    # The generated number is stored in Word numbering XML, not visible text, but
    # the heading must still count as a major numbered section.
    assert a.metadata['major_section_count']==4
    assert any(x.get('number_source')=='word_numbering' for x in a.metadata['major_sections'])


def test_10_contents_mismatch(tmp_path):
    p=build_base(tmp_path/'tocbad.docx',contents_mismatch=True)
    a=audit_document(p,tmp_path/'out','en')
    assert 'CONTENTS_HEADING_MISMATCH' in codes(a)


def test_11_table_prose_numerical_inconsistency(tmp_path):
    p=build_base(tmp_path/'numdiff.docx');add_numeric_inconsistency(p)
    a=audit_document(p,tmp_path/'out','en')
    fs=[f for f in a.findings if f.code=='TABLE_PROSE_NUMERIC_INCONSISTENCY']
    assert fs
    assert any(f.evidence.get('table_value')=='6.43' and f.evidence.get('prose_value')=='6.13' for f in fs)


def test_12_appendix_crossref_mismatch(tmp_path):
    p=build_base(tmp_path/'appbad.docx');add_appendix_reference_without_appendix(p)
    a=audit_document(p,tmp_path/'out','en')
    assert 'APPENDIX_REFERENCE_MISMATCH' in codes(a)
    assert a.components['appendices'].status.value=='MISSING'


def test_13_numbered_lists_do_not_become_major_sections(tmp_path):
    p=build_base(tmp_path/'listnoise.docx');add_numbered_lists_that_are_not_major_sections(p)
    a=audit_document(p,tmp_path/'out','en')
    assert a.metadata['major_section_count']==3
    assert [x['number'] for x in a.metadata['major_sections']]==[1,2,3]
    assert 'SECTION_NUMBERING_GAPS' not in codes(a)


def test_14_caption_association_skips_blanks_and_joins_wrap(tmp_path):
    p=build_base(tmp_path/'captionwrap.docx');add_caption_with_blank_and_wrap(p)
    a=audit_document(p,tmp_path/'out','en')
    assert 'DUPLICATE_TABLE_NUMBERS' in codes(a)
    caps=[t.caption for t in a.tables if t.number==10]
    assert any(c and 'в швейной компании' in c for c in caps)


def test_15_narrow_index_column_is_not_broken(tmp_path):
    p=build_base(tmp_path/'indexcol.docx');add_narrow_index_column_table(p)
    a=audit_document(p,tmp_path/'out','en')
    target=[t for t in a.tables if t.number==20][0]
    assert target.risk!=TableRisk.BROKEN_REQUIRES_REVIEW


def test_16_malformed_figure_caption_still_detects_duplicate(tmp_path):
    p=build_base(tmp_path/'figartefact.docx');add_malformed_duplicate_figure_caption(p)
    a=audit_document(p,tmp_path/'out','en')
    assert 'DUPLICATE_FIGURE_NUMBERS' in codes(a)


def test_17_repeated_metric_value_inconsistency(tmp_path):
    p=build_base(tmp_path/'metricdiff.docx');add_repeated_metric_inconsistency(p)
    a=audit_document(p,tmp_path/'out','en')
    fs=[f for f in a.findings if f.code=='REPEATED_METRIC_VALUE_INCONSISTENCY']
    assert fs
    assert set(fs[0].evidence['values']) >= {1.72,4.4,5.0}


def test_18_unused_footnotes_part_does_not_count_as_footnote_system(tmp_path):
    p=build_base(tmp_path/'unusednotes.docx');add_unused_footnotes_part(p)
    a=audit_document(p,tmp_path/'out','en')
    assert a.preflight.footnotes_present is False
    assert a.references.system!=CitationSystem.FOOTNOTE


def test_19_takim_obrazom_counts_as_section_conclusion(tmp_path):
    p=build_base(tmp_path/'synthesis.docx');replace_section_conclusion_markers_with_takim_obrazom(p)
    a=audit_document(p,tmp_path/'out','en')
    assert 'SECTION_CONCLUSIONS_MISSING' not in codes(a)
