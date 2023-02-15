from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)