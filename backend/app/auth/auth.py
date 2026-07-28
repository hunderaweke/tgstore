from datetime import datetime, timedelta, timezone
from enum import Enum

import jwt
from app.schemas.user import TokenResponse
from app.settings.settings import get_settings
from jwt import InvalidTokenError
from pydantic import UUID4, BaseModel

settings = get_settings()


class TokenExpiredError(Exception):
    pass


class TokenType(str, Enum):
    REFRESH_TOKEN = "refresh"
    ACCESS_TOKEN = "access"


class TokenData(BaseModel):
    user_id: UUID4
    expire: float
    token_type: TokenType


def _create_token(user_id: UUID4, token_type: TokenType, expiry: timedelta) -> str:
    token_data = TokenData(
        user_id=user_id,
        expire=(datetime.now(timezone.utc) + expiry).timestamp(),
        token_type=token_type,
    )
    return jwt.encode(
        token_data.model_dump(mode="json"),
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_tokens(user_id: UUID4) -> TokenResponse:
    access_token = _create_token(
        user_id,
        TokenType.ACCESS_TOKEN,
        timedelta(hours=settings.ACCESS_TOKEN_EXPIRY_HOURS),
    )
    refresh_token = _create_token(
        user_id,
        TokenType.REFRESH_TOKEN,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRY_DAYS),
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def validate_token(token: str, token_type: TokenType) -> TokenData:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    token_data = TokenData.model_validate(payload)
    if token_data.token_type != token_type:
        raise InvalidTokenError("invalid token")
    if token_data.expire < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredError("expired token")
    return token_data


def refresh_access_token(refresh_token: str) -> TokenResponse:
    token_data = validate_token(refresh_token, TokenType.REFRESH_TOKEN)
    return create_tokens(token_data.user_id)
