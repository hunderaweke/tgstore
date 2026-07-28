import asyncio
import httpx
import hashlib
from pathlib import Path, PurePosixPath
from typing import AsyncIterator, Iterable
from app.settings.settings import get_settings
from fastapi import UploadFile
from pydantic import BaseModel
from app.schemas.file import FileChunkBase
from app.core import upload_file_to_telegram

settings = get_settings()
# 2 GB (decimal). Just under the self-hosted Bot API upload cap (~2000 MB), so
# a <=2 GB file is stored as a single chunk and only larger files are split.
# Downloads read chunks off the server's disk (--local mode), so the 20 MB
# cloud download cap does not apply here.
CHUNK_SIZE = 100_000_000  # 2 GB

# Block size for streaming a chunk off disk to the HTTP client.
STREAM_BLOCK_SIZE = 4 * 1024 * 1024  # 4 MB


def get_file_path(filename: str) -> Path:
    file_dir = Path(settings.UPLOAD_DIR) / filename
    file_dir.parent.mkdir(parents=True, exist_ok=True)
    return file_dir


class TelegramResultResponse(BaseModel):
    message_id: int
    document: TelegramFileResponse


class TelegramFileResponse(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int


async def save_upload_file(
    upload_file: UploadFile,
) -> tuple[int, list[FileChunkBase]]:
    size = 0
    index = 0
    chunks = []
    while True:
        chunk = await upload_file.read(CHUNK_SIZE)
        if not chunk:
            break
        telegram_response = await upload_file_to_telegram(
            chunk, f"{upload_file.filename}_part_{index+1}"
        )
        chunk_info = FileChunkBase(
            chunk_index=index,
            chunk_size=telegram_response.media.document.size,
            chunk_hash=hashlib.sha256(chunk).hexdigest(),
            telegram_message_id=telegram_response.id,
        )
        chunks.append(chunk_info)
        size += len(chunk)
        index += 1
    if size == 0:
        raise ValueError("Uploaded file is empty.")
    return size, chunks


async def download_file_from_telegram(telegram_path: str):
    async with httpx.AsyncClient(timeout=None) as client:
        url = f"{settings.TELEGRAM_API_URL}/file/{settings.TELEGRAM_BOT_TOKEN}/{telegram_path}"
        response = await client.get(url)
    response.raise_for_status()
    print(response)


async def get_telegram_file_path(file_id: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{settings.TELEGRAM_API_URL}/bot{settings.TELEGRAM_BOT_TOKEN}/getFile",
            data={"file_id": file_id},
        )
    response.raise_for_status()
    result = response.json()["result"]
    file_path = result["file_path"]
    return file_path


def split_into_chunks(file_path: Path, chunk_size: int = CHUNK_SIZE) -> list[Path]:
    chunks = []
    with open(file_path, "rb") as file:
        index = 0
        while True:
            data = file.read(chunk_size)
            if not data:
                break

            chunk_file_path = file_path.parent / f"{file_path.stem}_part_{index}"
            with open(chunk_file_path, "wb") as chunk_file:
                chunk_file.write(data)
            chunk = {
                "path": chunk_file_path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "index": index,
            }
            print(chunk)
            chunks.append(chunk)
            index += 1

    return chunks


def merge_chunks(chunks: list[dict], output_file_path: Path) -> None:
    with open(output_file_path, "wb") as output_file:
        for chunk in chunks:
            with open(chunk["path"], "rb") as chunk_file:
                data = chunk_file.read()
            if not data:
                raise ValueError(f"Chunk {chunk['index']} is empty.")
            data_sha256 = hashlib.sha256(data).hexdigest()
            if data_sha256 != chunk["sha256"]:
                raise ValueError(f"Chunk {chunk['index']} has been tampered with.")
            output_file.write(data)
            chunk_file.close()
    output_file.close()
