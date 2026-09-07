from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
import uuid
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

import anyio
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dissertation_formatter.engine import audit_document
from dissertation_formatter.models import ComponentStatus
from dissertation_formatter.translations import display_component

from .i18n import LANGUAGES, get_text
from .storage import JobStore

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
RESULT_TTL_MINUTES = int(os.getenv("RESULT_TTL_MINUTES", "15"))
RESULT_TTL_SECONDS = RESULT_TTL_MINUTES * 60
TEMP_ROOT = Path(os.getenv("NARXOZ_TEMP_ROOT", str(Path(tempfile.gettempdir()) / "narxoz-dissertation-beta")))
MAX_CONCURRENT_JOBS = int(os.getenv("MAX_CONCURRENT_JOBS", "2"))

store = JobStore(TEMP_ROOT / "results", RESULT_TTL_SECONDS)
processing_slots = asyncio.Semaphore(MAX_CONCURRENT_JOBS)
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


def _lang(lang: str | None) -> str:
    return lang if lang in LANGUAGES else "en"


def _valid_docx(path: Path) -> bool:
    try:
        if not zipfile.is_zipfile(path):
            return False
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            return "[Content_Types].xml" in names and "word/document.xml" in names
    except (OSError, zipfile.BadZipFile):
        return False


def _safe_original_name(name: str | None) -> str:
    raw = Path(name or "dissertation.docx").name.replace("\x00", "")
    if not raw.lower().endswith(".docx"):
        raw += ".docx"
    return raw[:180]


def _status_copy(t: dict[str, str], status: str) -> tuple[str, str]:
    if status == "READY":
        return t["result_ready"], t["ready_text"]
    if status == "CONDITIONAL":
        return t["result_conditional"], t["conditional_text"]
    return t["result_resubmit"], t["resubmit_text"]


def _result_files(job_dir: Path, audit) -> dict[str, dict[str, str]]:
    files: dict[str, dict[str, str]] = {}
    if audit.formatted_path:
        source = Path(audit.formatted_path)
        target = job_dir / "FORMATTED_DISSERTATION.docx"
        shutil.move(str(source), target)
        files["formatted"] = {"name": target.name, "path": target.name}
    if audit.report_path:
        source = Path(audit.report_path)
        target_name = "NONCOMPLIANCE_REPORT.docx" if audit.status.value == "RESUBMIT" else "COMPLIANCE_REPORT.docx"
        target = job_dir / target_name
        shutil.move(str(source), target)
        files["report"] = {"name": target.name, "path": target.name}
    return files


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.root.mkdir(parents=True, exist_ok=True)
    store.cleanup_expired()
    yield
    store.shutdown()


app = FastAPI(
    title="Narxoz Master’s Dissertation Checker",
    version="0.1.0-beta",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")


@app.middleware("http")
async def privacy_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "engine": "v0.2", "web": "v0.1-beta"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request, lang: str = "en"):
    lang = _lang(lang)
    t = get_text(lang)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "lang": lang,
            "languages": LANGUAGES,
            "t": t,
            "max_mb": MAX_UPLOAD_MB,
            "ttl_minutes": RESULT_TTL_MINUTES,
        },
    )


@app.post("/process")
async def process_document(
    request: Request,
    language: str = Form("en"),
    dissertation: UploadFile = File(...),
):
    lang = _lang(language)
    t = get_text(lang)
    original_name = _safe_original_name(dissertation.filename)
    if not original_name.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail=t["invalid_docx"])

    job_id = uuid.uuid4().hex
    work_root = Path(tempfile.mkdtemp(prefix="narxoz-upload-"))
    input_path = work_root / original_name
    engine_out = work_root / "engine-output"
    job_dir: Path | None = None

    try:
        total = 0
        with input_path.open("wb") as dst:
            while True:
                chunk = await dissertation.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail=t["too_large"].format(max_mb=MAX_UPLOAD_MB))
                dst.write(chunk)
        await dissertation.close()

        if not _valid_docx(input_path):
            raise HTTPException(status_code=400, detail=t["invalid_docx"])

        async with processing_slots:
            audit = await anyio.to_thread.run_sync(
                lambda: audit_document(input_path, engine_out, lang, True)
            )

        # The student input is no longer needed after the engine has finished.
        input_path.unlink(missing_ok=True)

        job_dir = store.create(job_id)
        files = _result_files(job_dir, audit)

        # Audit JSON is an internal implementation artifact and may contain extracted
        # snippets. It is deliberately not retained by the web beta.
        for p in engine_out.glob("*_audit.json"):
            p.unlink(missing_ok=True)

        missing_components = [
            display_component(lang, c.name)
            for c in audit.components.values()
            if c.critical and c.applicable and c.status == ComponentStatus.MISSING
        ]
        meta = {
            "job_id": job_id,
            "language": lang,
            "original_name": original_name,
            "status": audit.status.value,
            "missing_critical_count": audit.missing_critical_count,
            "missing_components": missing_components,
            "files": files,
        }
        store.save_metadata(job_id, meta)
        store.schedule_expiry(job_id)
        return RedirectResponse(url=f"/result/{job_id}?lang={lang}", status_code=303)

    except HTTPException as exc:
        if job_dir is not None:
            store.delete(job_id)
        return templates.TemplateResponse(
            request,
            "error.html",
            {"lang": lang, "languages": LANGUAGES, "t": t, "message": str(exc.detail)},
            status_code=exc.status_code,
        )
    except Exception:
        if job_dir is not None:
            store.delete(job_id)
        return templates.TemplateResponse(
            request,
            "error.html",
            {"lang": lang, "languages": LANGUAGES, "t": t, "message": t["error_generic"]},
            status_code=500,
        )
    finally:
        try:
            await dissertation.close()
        except Exception:
            pass
        shutil.rmtree(work_root, ignore_errors=True)


@app.get("/result/{job_id}", response_class=HTMLResponse)
def result(request: Request, job_id: str, lang: str = "en"):
    lang = _lang(lang)
    t = get_text(lang)
    store.cleanup_expired()
    meta = store.load_metadata(job_id)
    if not meta:
        return templates.TemplateResponse(
            request,
            "error.html",
            {"lang": lang, "languages": LANGUAGES, "t": t, "message": t["expired"]},
            status_code=410,
        )
    status_title, status_text = _status_copy(t, meta["status"])
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "lang": lang,
            "languages": LANGUAGES,
            "t": t,
            "meta": meta,
            "status_title": status_title,
            "status_text": status_text,
            "ttl_minutes": RESULT_TTL_MINUTES,
        },
    )


@app.get("/download/{job_id}/{kind}")
def download(job_id: str, kind: str):
    store.cleanup_expired()
    meta = store.load_metadata(job_id)
    if not meta or kind not in meta.get("files", {}):
        raise HTTPException(status_code=404, detail="Temporary result not found")
    record = meta["files"][kind]
    path = store.job_dir(job_id) / record["path"]
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Temporary result not found")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=record["name"],
    )


@app.post("/delete/{job_id}")
def delete_result(job_id: str, language: str = Form("en")):
    lang = _lang(language)
    store.delete(job_id)
    return RedirectResponse(url=f"/?lang={lang}&deleted=1", status_code=303)
