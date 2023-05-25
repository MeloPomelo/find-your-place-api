import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from sqlmodel import text

from fastapi_async_sqlalchemy import db
from app.core.config import settings

from app.api.api import api_router


app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.DATABASE_URL,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 83,
        "max_overflow": 64,
    },
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Хе хе хе, потерялся?"}


async def add_postgresql_extension() -> None:
    async with db():
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        return await db.session.execute(query)


@app.on_event("startup")
async def on_startup():
    await add_postgresql_extension()
    print("startup fastapi")


add_pagination(app)
