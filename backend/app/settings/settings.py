from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "tgstore"
    VERSION: str = "0.1.0"
    DATABASE_URL: str

    REDIS_URL: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_API_URL: str = "https://api.telegram.org"
    STORAGE_CHAT_ID: int

    DEBUG: bool = True

    UPLOAD_DIR: str = "uploads"


@lru_cache
def get_settings() -> Settings:
    return Settings()
