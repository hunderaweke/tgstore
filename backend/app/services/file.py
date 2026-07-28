import mimetypes
from typing import AsyncIterator

from app.core.core import download_file_chunks
from app.models.file import File, FileChunk, FileStatus
from app.repositories.file import FileRepository
from app.schemas.file import FileCreate
from app.utils.file import save_upload_file
from fastapi import HTTPException, UploadFile, status


class FileService:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    async def create_file(self, file: FileCreate) -> File:
        db_file = File(**file.model_dump())
        return await self.repo.create(db_file)

    async def get_by_id(self, file_id: str, vault_id: str | None = None) -> File:
        result = await self.repo.get_with_chunks(file_id, vault_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="file not found"
            )

        return result

    async def list(self, offset: int, limit: int) -> list[File]:
        return await self.repo.list(offset, limit)

    async def delete(self, file_id: str):
        db_file = await self.get_by_id(file_id)
        await self.repo.delete(db_file)

    async def list_by_vault_id(self, vault_id: str) -> list[File]:
        return await self.repo.get_by_vault_id(vault_id)

    async def upload(self, vault_id: str, upload_file: UploadFile) -> File:
        mimetype = upload_file.content_type or (
            mimetypes.guess_type(upload_file.filename)[0] or "application/octet-stream"
        )
        db_file = File(
            vault_id=vault_id, filename=upload_file.filename, mimetype=mimetype
        )
        await self.repo.create(db_file)
        try:
            size, chunks = await save_upload_file(upload_file)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            ) from e
        for chunk in chunks:
            self.repo.session.add(
                FileChunk(
                    file_id=db_file.id,
                    chunk_index=chunk.chunk_index,
                    chunk_size=chunk.chunk_size,
                    chunk_hash=chunk.chunk_hash,
                    telegram_message_id=chunk.telegram_message_id,
                )
            )
        db_file.filesize = size
        db_file.status = FileStatus.STORED_LOCALLY
        await self.repo.session.flush()
        await self.repo.session.refresh(db_file, attribute_names=["chunks"])
        return db_file

    async def download(
        self, file_id: str, vault_id: str | None = None
    ) -> tuple[File, AsyncIterator[bytes]]:
        db_file = await self.get_by_id(file_id, vault_id)
        return db_file, download_file_chunks(db_file)
