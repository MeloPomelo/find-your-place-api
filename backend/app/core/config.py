import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_USER_PASSWORD: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    FIREBASE_URL: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)