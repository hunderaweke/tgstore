from .base import UUIDPkMixin, TimestampMixin, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .file import File
from sqlalchemy import ForeignKey


class Vault(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "vaults"

    name: Mapped[str] = mapped_column(nullable=False)
    files: Mapped[list["File"]] = relationship("File", back_populates="vault")
