from app.models.vault import Vault
from app.repositories.vault import VaultRepository
from app.schemas.vault import VaultCreate, VaultUpdate
from fastapi import HTTPException, status


class VaultService:
    def __init__(self, repo: VaultRepository):
        self.repo = repo

    async def create_vault(self, vault: VaultCreate) -> Vault:
        vault = Vault(**vault.model_dump())
        return await self.repo.create(vault)

    async def get_vault_by_id(self, vault_id: str) -> Vault:
        result = await self.repo.get(vault_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="vault not found",
            )
        return result

    async def list_vaults(self, offset: int = 0, limit: int = 0) -> list[Vault]:
        return await self.repo.list(offset, limit)

    async def delete_vault(self, vault_id: str) -> None:
        result = await self.get_vault_by_id(vault_id)
        await self.repo.delete(result)

    async def update(self, vault_id: str, data: VaultUpdate) -> Vault:
        vault = await self.get_vault_by_id(vault_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return vault
        return await self.repo.update(vault, update_data)
