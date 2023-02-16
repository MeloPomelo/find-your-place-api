import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware


from api.api import api_router
from fastapi_async_sqlalchemy import db
from sqlmodel import text

# from core.config import settings


app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    SQLAlchemyMiddleware,
    # db_url=settings.DATABASE_URL,
    db_url="",
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
    return {"message": "Hello there!"}


async def add_postgresql_extension() -> None:
    async with db():
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        return await db.session.execute(query)


@app.on_event("startup")
async def on_startup():
    await add_postgresql_extension()
    print("startup fastapi")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)