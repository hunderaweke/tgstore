from typing import Annotated

from app.database.database import get_db
from app.repositories.file import FileRepository
from app.repositories.vault import VaultRepository
from app.services.file import FileService
from app.services.vault import VaultService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vault_repository(session: Annotated[AsyncSession, Depends(get_db)]):
    return VaultRepository(session=session)


async def get_vault_service(
    repo: Annotated[VaultRepository, Depends(get_vault_repository)],
):
    return VaultService(repo=repo)


async def get_file_repository(session: Annotated[AsyncSession, Depends(get_db)]):
    return FileRepository(session=session)


async def get_file_service(
    repo: Annotated[FileRepository, Depends(get_file_repository)],
):
    return FileService(repo=repo)
