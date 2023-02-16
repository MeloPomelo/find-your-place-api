import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    DATABASE_URL: str
    
    FIREBASE_URL: str

    # class Config:
    #     case_sensitive = True
    #     env_file = os.path.expanduser("~/.env")


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)