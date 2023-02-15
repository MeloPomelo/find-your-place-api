from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)