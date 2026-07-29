from enum import Enum as PyEnum

from app.models.vault import Vault
from app.schemas.common import SortOrder
from sqlalchemy import func, select

from .base import BaseRepository


class VaultSortField(str, PyEnum):
    name = "name"
    created_at = "created_at"
    updated_at = "updated_at"


_SORT_COLUMNS = {
    VaultSortField.name: Vault.name,
    VaultSortField.created_at: Vault.created_at,
    VaultSortField.updated_at: Vault.updated_at,
}


class VaultRepository(BaseRepository[Vault]):
    def __init__(self, session):
        super().__init__(Vault, session)

    async def list_vaults(
        self,
        user_id: str,
        offset: int,
        limit: int,
        search: str | None = None,
        sort_by: VaultSortField = VaultSortField.created_at,
        sort_order: SortOrder = SortOrder.desc,
    ) -> tuple[list[Vault], int]:
        filters = [Vault.user_id == user_id]
        if search:
            filters.append(Vault.name.ilike(f"%{search}%"))

        count_result = await self.session.execute(
            select(func.count(Vault.id)).where(*filters)
        )
        total = count_result.scalar_one()

        column = _SORT_COLUMNS[sort_by]
        order = column.desc() if sort_order == SortOrder.desc else column.asc()

        result = await self.session.execute(
            select(Vault).where(*filters).order_by(order).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total
