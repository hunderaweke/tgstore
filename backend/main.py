from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.settings.settings import get_settings
from app.routes.vault import router as vault_router
from app.workers.worker import WorkerSettings, get_redis_pool

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await get_redis_pool()
    yield
    await app.state.redis.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(vault_router)
