from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    PROJECT_NAME: str = "tgstore"
    VERSION: str = "0.1.0"
    DATABASE_URL: str

    REDIS_URL: str

    TELEGRAM_API_ID: str
    TELEGRAM_API_HASH: str
    TELEGRAM_BOT_TOKEN: str
    STORAGE_CHAT_ID: int
    DEBUG: bool = True
    TELEGRAM_API_URL: str

    UPLOAD_DIR: str = "uploads"
    DOWNLOAD_DIR: str = "downloads"


@lru_cache
def get_settings() -> Settings:
    return Settings()
