from app.settings.settings import get_settings
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl

settings = get_settings()
oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


class GoogleOauthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: int
    email: EmailStr
    given_name: str
    family_name: str
    picture: HttpUrl
    
    
