from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from fastapi import HTTPException, status


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_or_get(self, data: UserCreate) -> User:
        result = await self.repo.get_by_email(data.email)
        if result:
            return result
        new_user = User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            picture=data.picture.unicode_string(),
        )
        new_user = await self.repo.create(new_user)
        return new_user

    async def get_by_id(self, user_id: str) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
        return user

    async def list_users(self, offset: int = 0, limit: int = 0) -> list[User]:
        users = await self.repo.list(offset, limit)
        return users

    async def delete_user(self, user_id: str):
        user = await self.get_by_id(user_id)
        return
