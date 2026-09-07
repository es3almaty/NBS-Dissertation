# Temporary beta deployment: GitHub + Netlify

## Architecture

The public beta URL is served by **Netlify**. Netlify proxies all routes to the existing **Python/FastAPI** application hosted on a small ephemeral backend service (the included `render.yaml` is configured for Render Free).

This keeps the validated Python dissertation engine unchanged. The Netlify layer does not make compliance decisions and cannot bypass the engine's READY / CONDITIONAL / RESUBMIT routing.

```text
Student browser
    |
    v
Netlify public beta URL
    |  HTTP 200 proxy
    v
FastAPI backend (Render)
    |
    v
v0.2 dissertation engine
```

There is no database. Uploads are temporary. Generated download files expire after 15 minutes by default.

## 1. Create the GitHub repository

Suggested repository name:

`narxoz-dissertation-beta`

Push the contents of this folder to the repository root and use `main` as the default branch.

GitHub Actions will run `pytest -q` on each push and pull request.

## 2. Deploy the Python backend

In Render:

1. New > Blueprint, or New > Web Service.
2. Connect the GitHub repository.
3. Use the included `render.yaml` / Dockerfile.
4. Select the Free instance for the temporary beta.
5. Wait for `/health` to return HTTP 200.
6. Copy the HTTPS service origin, for example:
   `https://narxoz-dissertation-beta-api.onrender.com`

The free service may spin down after inactivity, so the first request after an idle period can be slow. That is acceptable for the temporary beta, not for production.

## 3. Create the Netlify site from GitHub

In Netlify:

1. Add new project > Import an existing project > GitHub.
2. Select the same repository.
3. Netlify will read `netlify.toml` automatically.
4. Add one environment variable:

   `BACKEND_ORIGIN=https://YOUR-RENDER-SERVICE.onrender.com`

5. Deploy.

The Netlify build runs `netlify/build.sh`, which writes the proxy rule into the publish directory. The build deliberately fails if `BACKEND_ORIGIN` is absent or is not HTTPS.

## 4. Smoke test

Open the Netlify URL and verify:

1. Home page loads through the Netlify URL.
2. `/health` returns JSON with engine `v0.2`.
3. Upload an incomplete dissertation and confirm RESUBMIT produces only the non-compliance report.
4. Confirm the browser URL remains the Netlify domain during upload, result display, and download.
5. Confirm the generated files expire or delete after the configured TTL.

## 5. Temporary beta rule

Do not add a database, student accounts, document history, or analytics that capture dissertation content during this beta.

## Why not run FastAPI inside Netlify Functions?

The validated engine is Python and performs nontrivial DOCX/OOXML processing. Netlify's current Functions documentation centers on TypeScript/JavaScript and Go runtimes. Rewriting the engine merely to force it into a Netlify function would introduce unnecessary regression risk. Netlify is therefore used as the public deployment/front-door layer while the Python compute remains on a Python-capable service.
