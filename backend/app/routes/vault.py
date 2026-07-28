from typing import Annotated

from app.dependencies import get_file_service, get_vault_service
from app.schemas.file import FileResponse
from app.schemas.vault import VaultCreate, VaultResponse, VaultUpdate
from app.services.file import FileService
from app.services.vault import VaultService
from fastapi import Depends, UploadFile, status
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

router = APIRouter(prefix="/vaults", tags=["Vaults"])


@router.post("/", response_model=VaultResponse, status_code=status.HTTP_201_CREATED)
async def create_vault(
    vault: VaultCreate, service: Annotated[VaultService, Depends(get_vault_service)]
):
    new_vault = await service.create_vault(vault=vault)
    return new_vault


@router.get("/", response_model=list[VaultResponse])
async def list_vaults(
    vault_service: Annotated[VaultService, Depends(get_vault_service)],
):
    vaults = await vault_service.list_vaults()
    return vaults


@router.delete("/{vault_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vault(
    vault_id: str, vault_service: Annotated[VaultService, Depends(get_vault_service)]
):
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
    vault_id: str, vault_service: Annotated[VaultService, Depends(get_vault_service)]
):
    vault = await vault_service.get_vault_by_id(vault_id)
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
):
    await vault_service.get_vault_by_id(vault_id)
    db_file = await file_service.upload(vault_id, file)
    return db_file


@router.get(
    "/{vault_id}/files",
    response_model=list[FileResponse],
    status_code=status.HTTP_200_OK,
)
async def get_files(
    vault_id: str, file_service: Annotated[FileService, Depends(get_file_service)]
):
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
):
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
