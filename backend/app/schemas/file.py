from pydantic import BaseModel, Field, ConfigDict, UUID4


class FileBase(BaseModel):
    filename: str = Field(..., description="Name of the file")


class FileCreate(FileBase):
    pass


class FileResponse(FileBase):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: UUID4 = Field(..., description="ID of the file")
    filesize: int = Field(..., description="Size of the file in bytes")
    filepath: str = Field(..., description="Path where the file is stored")
    status: str = Field(..., description="Status of the file")
    vault_id: UUID4 = Field(..., description="ID of the vault the file belongs to")
    chunks: list[FileChunkResponse] | None = Field(
        ..., description="List of file chunks associated with the file"
    )


class FileChunkBase(BaseModel):
    chunk_index: int | None = Field(..., description="Index of the file chunk")
    chunk_size: int = Field(..., description="Size of the file chunk in bytes")
    chunk_hash: str = Field(..., description="SHA256 hash of the file chunk")
    telegram_message_id: int = Field(
        ..., description="Telegram message ID for the file chunk"
    )
    telegram_file_id: str = Field(
        ..., description="Telegram file ID for the file chunk"
    )
    telegram_unique_file_id: str = Field(
        ..., description="Telegram unique file ID for the file chunk"
    )


class FileChunkResponse(FileChunkBase):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: UUID4 = Field(..., description="ID of the file chunk")
