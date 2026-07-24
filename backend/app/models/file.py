from .base import UUIDPkMixin, TimestampMixin, Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, Enum
from enum import Enum as PyEnum


class FileStatus(PyEnum):
    RECEIVING = "RECEIVING"
    STORED_LOCALLY = "STORED_LOCALLY"
    QUEUED = "QUEUED"
    PUSHING = "PUSHING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class File(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(nullable=False)
    filesize: Mapped[int] = mapped_column(nullable=True, default=0)
    filepath: Mapped[str] = mapped_column(nullable=True, default="")
    status: Mapped[FileStatus] = mapped_column(
        Enum(FileStatus), nullable=False, default=FileStatus.RECEIVING
    )
    vault_id: Mapped[str] = mapped_column(
        ForeignKey("vaults.id"), nullable=False, index=True
    )
    vault: Mapped["Vault"] = relationship("Vault", back_populates="files")
