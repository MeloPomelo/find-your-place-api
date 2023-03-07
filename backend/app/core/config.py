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


    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings() 