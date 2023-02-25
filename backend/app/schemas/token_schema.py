from pydantic import BaseModel
from user_schema import UserRead


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: UserRead


class TokenRead(BaseModel):
    access_token: str
    token_type: str