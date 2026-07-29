from typing import Annotated

from app.auth.auth import TokenExpiredError, create_tokens, refresh_access_token
from app.auth.oauth import GoogleOauthResponse, oauth
from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.settings.settings import get_settings
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from jwt import InvalidTokenError

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def _set_auth_cookies(
    response: Response, access_token: str, refresh_token: str
) -> None:
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        samesite="lax",
        secure=not settings.DEVELOPMENT,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="lax",
        secure=not settings.DEVELOPMENT,
    )


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get(
    "/google/callback",
    name="google_callback",
    status_code=status.HTTP_200_OK,
)
async def google_callback(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        token = await oauth.google.authorize_access_token(request)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Oauth authorization failed"
        )
    userinfo = token.get("userinfo")
    if not userinfo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user data is sent by google",
        )
    userinfo = GoogleOauthResponse.model_validate(userinfo)
    user = UserCreate(
        first_name=userinfo.given_name,
        last_name=userinfo.family_name,
        email=userinfo.email,
        picture=userinfo.picture,
    )
    new_user = await user_service.create_or_get(user)
    tokens = create_tokens(new_user.id)
    response = RedirectResponse(
        url=f"{settings.FRONTEND_AUTH_REDIRECT_URI}", status_code=status.HTTP_302_FOUND
    )
    _set_auth_cookies(response, tokens.access_token, tokens.refresh_token)
    return response


@router.post("/refresh", status_code=status.HTTP_204_NO_CONTENT)
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    try:
        tokens = refresh_access_token(refresh_token)
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    _set_auth_cookies(response, tokens.access_token, tokens.refresh_token)
