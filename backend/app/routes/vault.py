from typing import Annotated
from app.schemas.vault import VaultCreate, VaultUpdate, VaultResponse
from app.models.vault import Vault
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from app.database.database import get_db

router = APIRouter(prefix="/vaults", tags=["Vaults"])


@router.post("/", response_model=VaultResponse, status_code=status.HTTP_201_CREATED)
async def create_vault(
    vault: VaultCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        existing_vault = await db.execute(
            select(Vault)
            .where(Vault.name == vault.name)
            .options(selectinload(Vault.files))
        )
        if existing_vault.scalar_one():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A vault with this name already exists.",
            )
    except Exception as e:
        pass

    new_vault = Vault(name=vault.name)
    db.add(new_vault)
    await db.commit()
    await db.refresh(new_vault, attribute_names=["files"])

    return new_vault


@router.get("/", response_model=list[VaultResponse])
async def list_vaults(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Vault).options(selectinload(Vault.files)))
    return result.scalars().all()


@router.delete("/{vault_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vault(vault_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Vault).where(Vault.id == vault_id))
    vault = result.scalar_one_or_none()

    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vault not found."
        )

    await db.delete(vault)
    await db.commit()


@router.put("/{vault_id}", response_model=VaultResponse)
async def update_vault(
    vault_id: str,
    vault_update: VaultUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Vault).where(Vault.id == vault_id))
    vault = result.scalar_one_or_none()

    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vault not found."
        )

    # Check for name uniqueness
    existing_vault = await db.execute(
        select(Vault)
        .where(Vault.name == vault_update.name, Vault.id != vault_id)
        .options(selectinload(Vault.files))
    )
    if existing_vault.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A vault with this name already exists.",
        )

    vault.name = vault_update.name
    await db.commit()
    await db.refresh(vault, attribute_names=["files"])

    return vault


@router.get("/{vault_id}", response_model=VaultResponse)
async def get_vault(vault_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(Vault).where(Vault.id == vault_id).options(selectinload(Vault.files))
    )
    vault = result.scalar_one_or_none()

    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vault not found."
        )

    return vault
