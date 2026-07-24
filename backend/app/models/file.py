from .base import UUIDPkMixin, TimestampMixin, Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey


class File(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(nullable=False)
    filesize: Mapped[int] = mapped_column(nullable=False)
    filepath: Mapped[str] = mapped_column(nullable=False)
    vault_id: Mapped[str] = mapped_column(
        ForeignKey("vaults.id"), nullable=False, index=True
    )
    vault: Mapped["Vault"] = relationship(
        "Vault", back_populates="files", cascade="all, delete-orphan"
    )
