import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_USER_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    DATABASE_URL: str
    
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_URL: str
    MINIO_BUCKET: str

    DB_POOL_SIZE = 83
    WEB_CONCURRENCY = 9
    POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)
    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings() 