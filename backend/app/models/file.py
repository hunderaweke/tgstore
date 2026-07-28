from enum import Enum as PyEnum

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDPkMixin


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
    mimetype: Mapped[str] = mapped_column(nullable=True, default="")
    status: Mapped[FileStatus] = mapped_column(
        Enum(FileStatus), nullable=False, default=FileStatus.RECEIVING
    )
    vault_id: Mapped[str] = mapped_column(
        ForeignKey("vaults.id"), nullable=False, index=True
    )
    vault: Mapped["Vault"] = relationship("Vault", back_populates="files")
    chunks: Mapped[list["FileChunk"]] = relationship(
        "FileChunk",
        cascade="all, delete-orphan",
        back_populates="file",
        order_by="FileChunk.chunk_index",
    )


class FileChunk(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "file_chunks"

    file_id: Mapped[str] = mapped_column(
        ForeignKey("files.id"), nullable=False, index=True
    )
    file: Mapped["File"] = relationship("File", back_populates="chunks")
    chunk_index: Mapped[int] = mapped_column(nullable=True)
    chunk_size: Mapped[int] = mapped_column(nullable=True)
    chunk_hash: Mapped[str] = mapped_column(nullable=True)
    telegram_message_id: Mapped[int] = mapped_column(Integer, nullable=True)
