from __future__ import annotations

import asyncio
import json
import shutil
import time
from pathlib import Path
from threading import Lock


class JobStore:
    """Ephemeral, filesystem-backed result store.

    Student uploads are not kept here. Only generated result files and a tiny
    metadata JSON are retained for the download window.
    """

    def __init__(self, root: Path, ttl_seconds: int):
        self.root = root
        self.ttl_seconds = ttl_seconds
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._expiry_tasks: dict[str, asyncio.Task] = {}

    def job_dir(self, job_id: str) -> Path:
        return self.root / job_id

    def create(self, job_id: str) -> Path:
        path = self.job_dir(job_id)
        path.mkdir(parents=True, exist_ok=False)
        return path

    def save_metadata(self, job_id: str, metadata: dict) -> None:
        metadata = dict(metadata)
        metadata["created_at"] = time.time()
        metadata["expires_at"] = time.time() + self.ttl_seconds
        (self.job_dir(job_id) / "job.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def load_metadata(self, job_id: str) -> dict | None:
        path = self.job_dir(job_id) / "job.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
        if time.time() >= float(data.get("expires_at", 0)):
            self.delete(job_id)
            return None
        return data

    def delete(self, job_id: str) -> None:
        with self._lock:
            shutil.rmtree(self.job_dir(job_id), ignore_errors=True)

    def cleanup_expired(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        now = time.time()
        for child in list(self.root.iterdir()):
            if not child.is_dir():
                continue
            meta = child / "job.json"
            expired = False
            if not meta.exists():
                expired = True
            else:
                try:
                    data = json.loads(meta.read_text(encoding="utf-8"))
                    expired = now >= float(data.get("expires_at", 0))
                except Exception:
                    expired = True
            if expired:
                shutil.rmtree(child, ignore_errors=True)

    def schedule_expiry(self, job_id: str) -> None:
        async def expire() -> None:
            try:
                await asyncio.sleep(self.ttl_seconds)
                self.delete(job_id)
            finally:
                self._expiry_tasks.pop(job_id, None)

        try:
            task = asyncio.create_task(expire())
            self._expiry_tasks[job_id] = task
        except RuntimeError:
            # No running event loop (e.g. some tests). Request-time cleanup still applies.
            pass

    def shutdown(self) -> None:
        # Privacy-first: delete all temporary result files when the process stops.
        shutil.rmtree(self.root, ignore_errors=True)
