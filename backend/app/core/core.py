import os, io
from telethon import TelegramClient
from app.settings.settings import get_settings
from app.models.file import File
from telethon.tl.types import (
    Message,
    InputDocumentFileLocation,
)

settings = get_settings()

telegram_app = TelegramClient(
    "bot_session", api_id=settings.TELEGRAM_API_ID, api_hash=settings.TELEGRAM_API_HASH
)


async def stream_telegram_chunks(message: Message):
    location = InputDocumentFileLocation(
        id=message.media.document.id,
        access_hash=message.media.document.access_hash,
        thumb_size="",
        file_reference=b"",
    )
    async for chunk in telegram_app.iter_download(file=location, chunk_size=256 * 1024):
        yield chunk


async def download_file_chunks(file: File):
    for chunk in file.chunks:
        message = await telegram_app.get_messages(
            settings.STORAGE_CHAT_ID, ids=chunk.telegram_message_id
        )
        if message is None or message.media is None:
            raise FileNotFoundError(f"Media not found")
        async for block in stream_telegram_chunks(message):
            yield block


async def upload_file_to_telegram(chunk: bytes, filename: str) -> Message:
    buffer = io.BytesIO(chunk)
    buffer.name = filename

    message = await telegram_app.send_file(
        settings.STORAGE_CHAT_ID, file=buffer, force_document=True
    )
    return message
