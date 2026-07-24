from fastapi import FastAPI
from app.settings.settings import get_settings
from app.routes.vault import router as vault_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME, debug=settings.DEBUG, version=settings.VERSION
)

app.include_router(vault_router)
