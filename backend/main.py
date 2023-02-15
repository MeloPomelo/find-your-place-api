import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.database import Base, engine
from app.api.coworking_router import *


Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coworking_router)


@app.get("/")
async def root():
    return {"message": "Hello there!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)