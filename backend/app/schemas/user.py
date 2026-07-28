from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, HttpUrl


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    picture: HttpUrl


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    refresh_token: str
    access_token: str
