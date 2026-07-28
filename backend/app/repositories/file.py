from app.models.file import File, FileChunk

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .base import BaseRepository


class FileRepository(BaseRepository[File]):
    def __init__(self, session):
        super().__init__(File, session)

    async def get_by_vault_id(self, vault_id: str) -> list[File]:
        result = await self.session.execute(
            select(File)
            .where(File.vault_id == vault_id)
            .options(selectinload(File.chunks))
        )
        return result.scalars().all()

    async def get_with_chunks(
        self, file_id: str, vault_id: str | None = None
    ) -> File | None:
        query = select(File).where(File.id == file_id).options(selectinload(File.chunks))
        if vault_id is not None:
            query = query.where(File.vault_id == vault_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
