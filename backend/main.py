from typing import Annotated

from app.core import download_file_chunks, telegram_app
from app.database.database import AsyncSession, get_db
from app.models.file import File
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.vault import router as vault_router
from app.settings.settings import get_settings
from app.workers.worker import get_redis_pool
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from starlette.middleware.sessions import SessionMiddleware

gen = get_db()
settings = get_settings()


@asynccontextmanager
async def get_db_ctx():
    async with get_db() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await get_redis_pool()
    await telegram_app.start(bot_token=settings.TELEGRAM_BOT_TOKEN)
    yield
    await app.state.redis.close()
    await telegram_app.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
    lifespan=lifespan,
)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)
app.include_router(vault_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/download/{file_id}")
async def download_file(file_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(File).where(File.id == file_id).options(selectinload(File.chunks))
    )
    file = result.scalar()
    return StreamingResponse(
        download_file_chunks(file),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file.filename}"',
        },
    )
