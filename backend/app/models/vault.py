from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDPkMixin
from .file import File
from .user import User


class Vault(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "vaults"

    name: Mapped[str] = mapped_column(nullable=False)
    files: Mapped[list["File"]] = relationship(
        "File", back_populates="vault", cascade="all, delete-orphan"
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=True, index=True
    )
