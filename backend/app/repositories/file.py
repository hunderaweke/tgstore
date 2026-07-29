from enum import Enum as PyEnum

from app.models.file import File, FileChunk, FileStatus
from app.schemas.common import SortOrder
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .base import BaseRepository


class FileSortField(str, PyEnum):
    filename = "filename"
    filesize = "filesize"
    created_at = "created_at"
    updated_at = "updated_at"


_SORT_COLUMNS = {
    FileSortField.filename: File.filename,
    FileSortField.filesize: File.filesize,
    FileSortField.created_at: File.created_at,
    FileSortField.updated_at: File.updated_at,
}


class FileRepository(BaseRepository[File]):
    def __init__(self, session):
        super().__init__(File, session)

    async def get_by_vault_id(
        self,
        vault_id: str,
        offset: int,
        limit: int,
        search: str | None = None,
        status: FileStatus | None = None,
        mimetype: str | None = None,
        sort_by: FileSortField = FileSortField.created_at,
        sort_order: SortOrder = SortOrder.desc,
    ) -> tuple[list[File], int]:
        filters = [File.vault_id == vault_id]
        if search:
            filters.append(File.filename.ilike(f"%{search}%"))
        if status is not None:
            filters.append(File.status == status)
        if mimetype:
            if mimetype.endswith("/"):
                filters.append(File.mimetype.ilike(f"{mimetype}%"))
            else:
                filters.append(File.mimetype == mimetype)

        count_result = await self.session.execute(
            select(func.count(File.id)).where(*filters)
        )
        total = count_result.scalar_one()

        column = _SORT_COLUMNS[sort_by]
        order = column.desc() if sort_order == SortOrder.desc else column.asc()

        result = await self.session.execute(
            select(File)
            .where(*filters)
            .options(selectinload(File.chunks))
            .order_by(order)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all()), total

    async def get_with_chunks(
        self, file_id: str, vault_id: str | None = None
    ) -> File | None:
        query = select(File).where(File.id == file_id).options(selectinload(File.chunks))
        if vault_id is not None:
            query = query.where(File.vault_id == vault_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
