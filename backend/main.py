from typing import Annotated
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.concurrency import asynccontextmanager
from app.settings.settings import get_settings
from app.routes.vault import router as vault_router
from app.workers.worker import WorkerSettings, get_redis_pool
from app.database.database import get_db, AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from app.models.file import File
from fastapi import Depends
from app.core import telegram_app, download_file_chunks

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

app.include_router(vault_router)


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
