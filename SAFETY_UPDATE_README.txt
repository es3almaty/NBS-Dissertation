NBS Dissertation Beta - post-format safety update

What changed
1. A post-format content-integrity gate now compares the original and formatted DOCX.
2. The formatted dissertation is released only if student text, table structure/text, images, hyperlinks, notes/comments and embedded content are unchanged.
3. If integrity fails, no formatted dissertation is released.
4. Title-page layout, including supervisor details stored in a table, is preserved from global body reformatting and the first front-matter heading is forced to start on a new page.
5. Dynamic Word TOCs are marked to refresh on open. Static/typed TOC page numbers are not guessed or rewritten; they are flagged for the student to update manually.
6. New regression tests cover the integrity guard, deliberate text tampering, static TOC detection, title-page table preservation, and blocked release on corruption.

Validation
- Full local test suite: 28 passed.
- Mustafin real-document check: post-format content integrity PASS.

Upload
Extract this ZIP and upload the CONTENTS of the repository folder to the root of the existing GitHub repository on main, replacing files with the same names. Do not create a second nested repository folder.
