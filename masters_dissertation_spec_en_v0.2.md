# Narxoz Master's Dissertation / Project Submission-Readiness and Compliance Specification

Version: 0.2  
Status: Beta engineering specification  
Internal working language: English  
Input: DOCX only  
Output languages: English, Russian, Kazakh  
Scope: Master's dissertations/projects only; the institutional Regulation supplied for this build is specifically titled for MBA/EMBA Master's projects (see Policy Ambiguities).

## 1. Product purpose

The product is a submission-readiness and dissertation-compliance engine with a second-stage formatting capability. It must first decide whether a dissertation is sufficiently complete and structurally safe to format. It must not beautify a structurally defective submission.

Processing sequence:

`DOCX integrity preflight -> critical completeness -> internal consistency -> safe formatting`

The engine is deterministic wherever possible. It never writes missing academic content, chooses between contradictory research values, or reconstructs absent bibliographic metadata.

## 2. Source hierarchy

Two institutional sources govern the beta:

1. **Narxoz Master's Project Regulation (2025)**. This is the controlling source.
2. **Narxoz APA 7 guidance (Academic Council Protocol No. 6, 28 November 2022)**. This is used only where the Regulation explicitly refers to it or is silent.

Conflict rule: **the Master's Project Regulation prevails over generic APA guidance.**

Examples:

- The Regulation's Master's-specific structure prevails over the APA guide's generic student-paper structure.
- The Regulation's appendix example is `Appendix 1`, `Appendix 2`, etc.; generic APA appendix lettering must not override it.
- The Regulation explicitly defers technical formatting to the Narxoz APA instruction, so A4, portrait, margins, font, line spacing, page-number position and reference formatting may be taken from that guide.

No web source is authoritative for institutional requirements in this build.

## 3. Institutional rules encoded in v0.2

### 3.1 Mandatory Master's structure

The Regulation requires: title page (Appendix 2 template), Contents, abbreviations where present, Project Summary, main part, Conclusion, list of used literature, and appendices. It also requires a three-language annotation set (Kazakh, Russian, English). The beta treats appendices as a critical component only when appendices are cited or clearly required by the submitted document, per the product rule supplied for v0.2.

The Regulation recommends 50-70 pages excluding appendices and annotations. This is advisory because Word pagination is renderer-dependent.

The main part should, **as a rule**, contain three sections with subsections, and each section should end with conclusions. A four-section structure is therefore flagged for supervisor/program confirmation, not automatically failed or rewritten.

### 3.2 Title page

The Regulation Appendix 2 template includes the institutional name, student's full name, project topic, educational-program code/name, `MASTER'S PROJECT`/equivalent degree wording, scientific supervisor, and Almaty/year. Presence and compliance are separate states: an incomplete title page is `PRESENT_NONCOMPLIANT`, not `MISSING`.

### 3.3 Contents

Contents must include main section/subsection headings and page numbers. Titles in the text must fully match titles in Contents; abbreviating them is not permitted. v0.2 performs a conservative text-match check and flags mismatches without rewriting headings.

### 3.4 Project Summary

The Project Summary is distinct from the three-language annotations. Under the Regulation it should cover relevance, practical significance, current state of the problem, degree of treatment in domestic/foreign literature, goal, tasks, research object and practical research base. v0.2 detects the component but does not generate or substantively evaluate its academic content.

### 3.5 Appendices

Where appendices are applicable, all must be cited in the main text and each must have a title such as `Appendix 1` and begin on a new page. A cited but absent appendix is a missing critical component. The engine must never invent one.

### 3.6 Technical formatting from Narxoz APA guidance

Where formatting is permitted, safe defaults are:

- A4 paper;
- portrait orientation;
- 2.54 cm margins on all sides;
- Times New Roman 12 pt, black, regular body text;
- double line spacing for ordinary body text;
- student page number in the header, right aligned;
- references on a separate page, double spaced, with 1.27 cm hanging indent;
- reference list alphabetized by first author where safely identifiable;
- tables numbered sequentially with Arabic numerals;
- table borders limited to lines necessary for clarity; no vertical borders or full grid by default;
- figures numbered sequentially with Arabic numerals.

The implementation deliberately preserves complex tables rather than aggressively imposing border/style changes that could damage readability.

## 4. Gate 1: DOCX integrity/preflight

The engine opens the DOCX as both a Word document model and an OOXML ZIP package. It records or detects:

- paragraphs and paragraph styles;
- Word automatic numbering (`w:numId`, `w:ilvl`, numbering definitions, style numbering);
- heading candidates and outline-like structure;
- section count and section breaks;
- headers and footers;
- existing PAGE fields and duplicate PAGE fields;
- Word tables;
- captions near tables/figures;
- media/images;
- field instructions;
- hyperlinks;
- footnotes/endnotes parts;
- appendices and cross-reference text;
- Office Math equation objects where present.

The preflight must not flatten the document to plain text before structural inspection.

A corrupt/non-DOCX package is an execution error and is unsafe to format.

## 5. Gate 2: critical completeness

Each critical applicable component receives one of:

- `PRESENT_COMPLIANT`
- `PRESENT_NONCOMPLIANT`
- `MISSING`

Critical components:

1. Title page
2. Contents
3. Project Summary
4. Three-language annotation set (Kazakh, Russian, English)
5. Main body
6. Conclusion
7. References
8. Appendices, when cited or clearly required

A partially present component is not automatically `MISSING`.

### 5.1 Cutoff

If **more than two** applicable critical components are `MISSING`:

- submission state = `RESUBMIT`;
- formatting is not performed;
- only a full `NONCOMPLIANCE_REPORT.docx` is created.

The report still audits the entire document so the student can correct all identified issues in one cycle.

### 5.2 Submission states

`READY`: sufficiently complete, with no major unresolved student action. Output formatted DOCX + compliance report.

`CONDITIONAL`: no cutoff, but unresolved student actions remain. Output formatted DOCX + compliance report. Exactly two missing critical components is therefore eligible for formatting but remains conditional.

`RESUBMIT`: more than two critical components are missing, or the DOCX is technically unsafe to process. Output non-compliance report only.

## 6. Gate 3: internal-consistency checks

This layer checks the dissertation against itself. It does not fact-check externally and does not decide which conflicting value is correct.

Implemented deterministic checks include:

- table/prose numerical inconsistency where the same metric and year can be conservatively aligned;
- duplicate table numbers;
- table-number gaps;
- duplicate figure numbers;
- figure-number gaps;
- visible section-number gaps;
- references to nonexistent sections;
- references to nonexistent tables or figures;
- references to absent appendices;
- Contents entries that do not conservatively match actual headings;
- empty source placeholders such as `источник []`;
- missing section-conclusion signals;
- cited appendices without matching appendix headings.

Where alignment is ambiguous, preserve and flag rather than infer.

Future deterministic extensions should cover mechanically unambiguous totals, sample-size consistency, percentage totals and caption/title alignment without increasing false-positive rates.

## 7. Reference handling

Citation-system states:

- `APA_AUTHOR_DATE`
- `NUMERIC`
- `FOOTNOTE`
- `MIXED`
- `NO_DETECTABLE_SYSTEM`

References-section presence is assessed independently from citation system.

If numeric citations exist but no References section exists:

- References = `MISSING`;
- all detected numeric citation numbers are reported;
- no bibliography is reconstructed or inferred.

Where a list exists, v0.2 can apply safe physical formatting and identify conservative unmatched/duplicate signals. It does not verify that a source exists or that a citation supports a claim.

Required responsibility statement:

> References have been formatted using the information supplied in the dissertation. The system has not verified that the sources exist, that bibliographic information is accurate, or that the citations accurately represent the cited material. Responsibility for reference accuracy remains with the student.

## 8. Table handling

Every real Word table is classified:

- `SIMPLE_SAFE`
- `COMPLEX_SAFE_TO_PRESERVE`
- `BROKEN_REQUIRES_REVIEW`

Risk signals include merged cells, very large tables, excessive column count, extremely narrow grid columns, and cell text fragmented into many one/two-character lines. Broken tables are preserved and prominently flagged. Data is never changed.

Table/figure renumbering and prose cross-reference rewriting are conditional transformations and are not performed unless a future version can prove an unambiguous mapping.

## 9. Pagination and fields

Before adding page numbers the engine inspects PAGE fields in document/header/footer XML. If duplicate PAGE fields exist in a header/footer part, safe formatting retains one and removes extras. A page field is inserted only when no PAGE field exists. The default student location is the right-aligned header.

## 10. Transformation safety classes

### 10.1 Safe automatic transformations

- A4 and portrait orientation;
- 2.54 cm margins;
- Times New Roman 12 pt, black body text;
- double spacing in ordinary prose;
- conservative ordinary-paragraph first-line indentation;
- PAGE-field de-duplication and insertion when absent;
- reference hanging indents;
- simple layout normalization that does not alter data/content.

### 10.2 Conditional transformations

Only when mapping is unambiguous:

- table/figure renumbering;
- prose cross-reference updates;
- appendix renumbering;
- complex caption restructuring;
- bibliography sorting/restructuring where entries can be safely bounded;
- citation-style conversion.

Default when uncertain: **preserve and flag**.

### 10.3 Prohibited automatic transformations

Never invent sources, authors, dates, DOIs or publishers; write missing sections, Project Summary or annotations; rewrite literature review or argument; change findings; decide which conflicting number is correct; alter interpretation; reorganize the intellectual argument; verify sources using the web; or perform plagiarism/AI-writing detection as part of this formatter.

## 11. Compliance report

The report is always DOCX and contains:

1. Submission status
2. Executive summary
3. Critical structural requirements
4. Automatically corrected items
5. Student action required
6. Detected but not safely alterable
7. Internal inconsistencies requiring student review
8. Tables and figures
9. References and citations
10. Length and structural recommendations
11. Items not checked by the system
12. Student responsibility statement
13. Resubmission checklist where applicable

For `RESUBMIT`, the first page must make the status unmistakable and explain that formatting was not performed.

## 12. Privacy and retention

Beta architecture assumes:

`upload -> temporary processing -> outputs -> download -> deletion`

No student dissertation archive, no long-term retention and no unrelated reuse of dissertation content. The local CLI build writes only the explicitly requested output directory; a web deployment must use per-job temporary storage and delete it after the download window.

## 13. Regression policy

All student files pass through the same engine. No dissertation-specific patches are permitted. Real regression fixtures are Samatov and Sultanberdieva. Expected high-level state for both under the v0.2 cutoff is `RESUBMIT`.

Synthetic unit tests must cover the 12 acceptance scenarios listed in the transfer specification, including real OOXML numbering and PAGE-field fixtures.

## 14. Known policy ambiguities / deferred decisions

1. **Institutional scope.** The supplied 2025 Regulation is titled specifically for the degree of Master of Business Administration (MBA/EMBA), while the product brief says Master's dissertations/projects generally. v0.2 therefore does not claim that this rule set is valid for every Narxoz Master's program outside the supplied regulation's scope without an additional institutional source or explicit policy decision.
2. **Kazakh report wording.** Kazakh UI/report translations in v0.2 are functional engineering translations, not a separately supplied Narxoz-approved terminology sheet. Institutional language review is advisable before production.
3. **Appendix criticality.** Regulation 7.7 lists appendices as mandatory, while the v0.2 product rule makes appendices critical only when cited or clearly required. The engine follows the explicit v0.2 product rule and records the distinction.
4. **Paragraph first-line indent.** The supplied APA snippets establish double spacing and a 1.27 cm hanging indent for references, but do not provide a clearly retrieved general-body numeric first-line indent. v0.2 uses 1.27 cm conservatively for ordinary prose as an implementation default; this should be confirmed against the full institutional guide before production hard-freeze.
