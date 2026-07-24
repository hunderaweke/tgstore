from arq import create_pool
from arq.connections import RedisSettings
from app.settings.settings import get_settings
from app.utils.file import upload_file_to_telegram

settings = get_settings()


async def get_redis_pool():
    return await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))


async def push_to_telegram(ctx, file_path: str, filename: str):
    await upload_file_to_telegram(file_path, filename)


class WorkerSettings:
    functions = [push_to_telegram]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
