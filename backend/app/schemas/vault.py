from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, UUID4


class Base(BaseModel):
    pass


class VaultBase(Base):
    name: str = Field(..., description="Name of the vault")


class VaultCreate(VaultBase):
    pass


class VaultUpdate(VaultBase):
    pass


class VaultResponse(VaultBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="ID of the vault")
    created_at: datetime = Field(..., description="Creation timestamp of the vault")
    updated_at: datetime = Field(..., description="Last update timestamp of the vault")
    files: list[UUID4] | None = Field(
        ..., description="List of file IDs associated with the vault"
    )
