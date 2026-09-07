# Narxoz Master’s Dissertation Checker — Temporary Web Beta

GitHub-deployable beta of the Narxoz Master’s dissertation submission-readiness/compliance engine.

## Deployment model

- **GitHub**: canonical source repository and CI.
- **Netlify**: public temporary-beta URL and reverse proxy.
- **Render Free**: Python/FastAPI compute backend.
- **No database**.
- **No dissertation retention after processing**; generated result files are temporary.

The web layer cannot override the engine's `>2` missing-critical-component cutoff.

For exact deployment steps see [`DEPLOY_GITHUB_NETLIFY.md`](DEPLOY_GITHUB_NETLIFY.md).

## Student workflow

1. Select English, Russian, or Kazakh.
2. Upload one `.docx` Master’s dissertation/project.
3. The backend runs the same v0.2 engine used in regression testing.
4. Engine-controlled output:
   - `READY` → formatted dissertation + compliance report
   - `CONDITIONAL` → formatted dissertation + compliance report
   - `RESUBMIT` → non-compliance report only
5. Student downloads the generated output(s).

## Privacy / retention

- No database.
- No student account or document history.
- Uploaded dissertation is stored only in a temporary working directory.
- Input DOCX is deleted immediately after engine processing finishes.
- Internal audit JSON is not exposed or retained by the web beta.
- Generated outputs remain temporarily for **15 minutes by default**, then are deleted.
- User can delete results immediately from the result page.
- Temporary results are deleted on backend shutdown.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Test

```bash
python scripts/check_repo.py
pytest -q
```

GitHub Actions runs the same checks on pushes and pull requests.

## Scope

- Master’s dissertations/projects only
- DOCX input only
- Narxoz institutional rule hierarchy
- no academic-content writing
- no plagiarism or AI-writing detection
- no external reference verification
