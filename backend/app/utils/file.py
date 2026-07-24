import os
import httpx
import hashlib
from pathlib import Path
from app.settings.settings import get_settings
from fastapi import UploadFile

settings = get_settings()


def get_file_path(filename: str) -> Path:
    file_dir = Path(settings.UPLOAD_DIR) / filename
    file_dir.parent.mkdir(parents=True, exist_ok=True)
    return file_dir


async def save_upload_file(upload_file: UploadFile) -> tuple[Path, int, str]:
    dest = get_file_path(upload_file.filename)
    hasher = hashlib.sha256()
    size = 0
    with open(dest, "wb") as buffer:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)
            hasher.update(chunk)
            size += len(chunk)
    if size == 0:
        os.remove(dest)
        raise ValueError("Uploaded file is empty.")
    return dest, size, hasher.hexdigest()


async def upload_file_to_telegram(file_path: Path, filename: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        with open(file_path, "rb") as file:
            files = {"document": (filename, file)}
            response = await client.post(
                f"{settings.TELEGRAM_API_URL}/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument",
                data={"chat_id": settings.STORAGE_CHAT_ID},
                files=files,
            )

    response.raise_for_status()
    os.remove(file_path)
    print(response.json())
    return response.json()["result"]
