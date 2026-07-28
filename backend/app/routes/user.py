from typing import Annotated

from app.dependencies import get_current_user
from app.schemas.user import UserResponse
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: UserResponse = Depends(get_current_user)):
    return user
