from typing import Annotated

from app.auth.auth import TokenExpiredError, TokenType, validate_token
from app.database.database import get_db
from app.models.user import User
from app.repositories.file import FileRepository
from app.repositories.user import UserRepository
from app.repositories.vault import VaultRepository
from app.services.file import FileService
from app.services.user import UserService
from app.services.vault import VaultService
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

cookie_schema = APIKeyCookie(name="access_token", auto_error=False)


async def get_vault_repository(session: Annotated[AsyncSession, Depends(get_db)]):
    return VaultRepository(session=session)


async def get_vault_service(
    repo: Annotated[VaultRepository, Depends(get_vault_repository)],
):
    return VaultService(repo=repo)


async def get_file_repository(session: Annotated[AsyncSession, Depends(get_db)]):
    return FileRepository(session=session)


async def get_file_service(
    repo: Annotated[FileRepository, Depends(get_file_repository)],
):
    return FileService(repo=repo)


async def get_user_repository(session: Annotated[AsyncSession, Depends(get_db)]):
    return UserRepository(session=session)


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(repo=repo)


async def get_current_user(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    access_token: Annotated[str, Depends(cookie_schema)],
) -> User:
    try:
        token_data = validate_token(
            token=access_token, token_type=TokenType.ACCESS_TOKEN
        )
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    user_id = token_data.user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found"
        )
    return user
