# Beta validation record

Date: 2026-09-07

## Engine baseline

The web beta embeds the same v0.2 dissertation engine used in the preceding command-line tests.

- Original engine synthetic suite rerun before web build: **12/12 passed**.
- Web-layer test suite: **4/4 passed**.

## Web-layer checks

The automated web tests verify:

1. health endpoint and Russian UI render;
2. invalid/non-DOCX upload rejection;
3. `RESUBMIT` routing never exposes a formatted dissertation;
4. a sufficiently complete test DOCX exposes formatted dissertation + compliance report;
5. generated DOCX downloads are valid ZIP/OOXML files;
6. explicit deletion invalidates the temporary result.

## Real dissertation integration check

The exact uploaded `Алескеров В..docx` was submitted through the FastAPI upload route in Russian.

Observed result:

- HTTP upload completed and redirected to a result page;
- status page displayed `ИСПРАВИТЬ И ПОВТОРНО ЗАГРУЗИТЬ`;
- **no formatted-dissertation download was exposed**;
- a non-compliance-report download was exposed and returned a valid DOCX.

The student dissertation itself is **not included in this build**.

## Privacy behavior checked in code

- source upload is processed in an OS temporary work directory;
- source DOCX is deleted immediately after engine execution;
- internal audit JSON is not retained by the web app;
- only generated download files and minimal job metadata survive temporarily;
- default result TTL is 15 minutes;
- users can delete temporary results immediately;
- temporary result storage is cleared when the application process shuts down.

## Visual QA limitation

The HTML/CSS routes were served successfully and inspected structurally. Automated browser screenshot QA was not completed because the runtime has the Playwright Python package but no installed browser binary. This does not affect backend/API validation.

## GitHub / Netlify packaging

Deployment packaging adds no compliance logic. `netlify/build.sh` creates only a reverse-proxy configuration to the Python backend. The Python engine remains authoritative for READY / CONDITIONAL / RESUBMIT decisions.

Repository CI: `.github/workflows/test.yml`.
Backend deployment: `render.yaml` and `Dockerfile`.
Netlify deployment: `netlify.toml` + `netlify/build.sh`.
