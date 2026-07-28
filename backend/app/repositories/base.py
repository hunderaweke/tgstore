from typing import Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):

        self.model = model
        self.session = session

    async def get(self, id: str) -> Optional[ModelType]:
        return await self.session.get(self.model, id)

    async def list(self, offset: int = 0, limit: int = 0) -> list[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def create(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.flush

    async def update(self, obj: ModelType, data: dict) -> ModelType:
        for field, value in data.items():
            setattr(obj, field, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
