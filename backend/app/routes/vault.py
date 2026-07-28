from typing import Annotated

from app.dependencies import get_current_user, get_file_service, get_vault_service
from app.schemas.file import FileResponse
from app.schemas.user import UserResponse
from app.schemas.vault import VaultCreate, VaultResponse, VaultUpdate
from app.services.file import FileService
from app.services.vault import VaultService
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/vaults", tags=["Vaults"])


@router.post("/", response_model=VaultResponse, status_code=status.HTTP_201_CREATED)
async def create_vault(
    vault: VaultCreate,
    service: Annotated[VaultService, Depends(get_vault_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    new_vault = await service.create_vault(vault_data=vault, user_id=current_user.id)
    return new_vault


@router.get("/", response_model=list[VaultResponse])
async def list_vaults(
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
):
    vaults = await vault_service.list_vaults()
    return vaults


@router.delete("/{vault_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vault(
    vault_id: str,
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
    user: Annotated[UserResponse, Depends(get_current_user)],
):
    await vault_service.get_vault_by_id(vault_id, user.id)
    await vault_service.delete_vault(vault_id=vault_id)


@router.put("/{vault_id}", response_model=VaultResponse)
async def update_vault(
    vault_id: str,
    vault_update: VaultUpdate,
    service: Annotated[VaultService, Depends(get_vault_service)],
):
    vault = await service.update(vault_id, vault_update)
    return vault


@router.get("/{vault_id}", response_model=VaultResponse)
async def get_vault(
    vault_id: str,
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
    user: Annotated[UserResponse, Depends(get_current_user)],
):
    vault = await vault_service.get_vault_by_id(vault_id, user.id)
    return vault


@router.post(
    "/{vault_id}/files",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file_to_vault(
    vault_id: str,
    file: UploadFile,
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
    file_service: Annotated[FileService, Depends(get_file_service)],
    user: Annotated[UserResponse, Depends(get_current_user)],
):
    await vault_service.get_vault_by_id(vault_id, user.id)
    db_file = await file_service.upload(vault_id, file)
    return db_file


@router.get(
    "/{vault_id}/files",
    response_model=list[FileResponse],
    status_code=status.HTTP_200_OK,
)
async def get_files(
    vault_id: str,
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
    file_service: Annotated[FileService, Depends(get_file_service)],
    user: Annotated[UserResponse, Depends(get_current_user)],
):
    await vault_service.get_vault_by_id(vault_id, user.id)
    return await file_service.list_by_vault_id(vault_id)


@router.get(
    "/{vault_id}/files/{file_id}",
    response_model=FileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_file(
    vault_id: str,
    file_id: str,
    file_service: Annotated[FileService, Depends(get_file_service)],
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
    user: Annotated[UserResponse, Depends(get_current_user)],
):
    await vault_service.get_vault_by_id(vault_id, user.id)
    return await file_service.get_by_id(file_id, vault_id)


@router.get("/{vault_id}/files/{file_id}/download")
async def download_file(
    vault_id: str,
    file_id: str,
    file_service: Annotated[FileService, Depends(get_file_service)],
):
    db_file, chunks = await file_service.download(file_id, vault_id)
    return StreamingResponse(
        chunks,
        media_type=db_file.mimetype or "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{db_file.filename}"',
            "Content-Length": str(db_file.filesize),
        },
    )
