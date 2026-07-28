from sqlalchemy import select
from app.models.vault import Vault
from .base import BaseRepository


class VaultRepository(BaseRepository[Vault]):
    def __init__(self, session):
        super().__init__(Vault, session)
