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

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    SESSION_SECRET: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRY_HOURS: int
    REFRESH_TOKEN_EXPIRY_DAYS: int
    JWT_ALGORITHM: str

    USING_HTTPS: bool = False
    UPLOAD_DIR: str = "uploads"
    DOWNLOAD_DIR: str = "downloads"


@lru_cache
def get_settings() -> Settings:
    return Settings()
