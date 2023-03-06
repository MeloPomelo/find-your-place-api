from pydantic import BaseModel
from enum import Enum
from app.schemas.user_schema import UserRead


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: UserRead


class TokenRead(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"