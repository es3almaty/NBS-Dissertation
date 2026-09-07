# Synthetic regression results

Executed 19 scenarios through the same v0.2 engine. Pytest acceptance suite: 19/19 passed.

| Fixture | Status | Missing critical | Formatted | Major sections | Footnotes | Key findings |
|---|---:|---:|---:|---:|---:|---|
| 01_fully_compliant.docx | READY | 0 | yes | 3 | no | none |
| 02_two_missing.docx | CONDITIONAL | 2 | yes | 3 | no | none |
| 03_three_missing.docx | RESUBMIT | 3 | no | 3 | no | none |
| 04_unmatched_citation.docx | CONDITIONAL | 0 | yes | 3 | no | UNMATCHED_CITATIONS |
| 05_numeric_no_bibliography.docx | CONDITIONAL | 1 | yes | 3 | no | CONTENTS_HEADING_MISMATCH, NUMERIC_CITATIONS_NO_BIBLIOGRAPHY |
| 06_duplicate_tables.docx | CONDITIONAL | 0 | yes | 3 | no | DUPLICATE_TABLE_NUMBERS |
| 07_broken_table.docx | CONDITIONAL | 0 | yes | 3 | no | BROKEN_TABLE |
| 08_duplicate_page_fields.docx | READY | 0 | yes | 3 | no | DUPLICATE_PAGE_FIELDS |
| 09_automatic_numbering.docx | CONDITIONAL | 0 | yes | 4 | no | AUTOMATIC_WORD_NUMBERING_DETECTED, NORMAL_THREE_SECTION_STRUCTURE, SECTION_CONCLUSIONS_MISSING |
| 10_contents_mismatch.docx | CONDITIONAL | 0 | yes | 3 | no | CONTENTS_HEADING_MISMATCH |
| 11_numeric_inconsistency.docx | CONDITIONAL | 0 | yes | 3 | no | TABLE_PROSE_NUMERIC_INCONSISTENCY |
| 12_appendix_mismatch.docx | CONDITIONAL | 1 | yes | 3 | no | APPENDIX_REFERENCE_MISMATCH |
| 13_numbered_list_noise.docx | READY | 0 | yes | 3 | no | none |
| 14_caption_blank_wrap.docx | CONDITIONAL | 0 | yes | 3 | no | DUPLICATE_TABLE_NUMBERS |
| 15_narrow_index_column.docx | READY | 0 | yes | 3 | no | none |
| 16_malformed_figure_caption.docx | CONDITIONAL | 0 | yes | 3 | no | DUPLICATE_FIGURE_NUMBERS |
| 17_repeated_metric_inconsistency.docx | CONDITIONAL | 0 | yes | 3 | no | REPEATED_METRIC_VALUE_INCONSISTENCY |
| 18_unused_footnotes_part.docx | READY | 0 | yes | 3 | no | none |
| 19_section_synthesis_phrase.docx | READY | 0 | yes | 3 | no | none |
