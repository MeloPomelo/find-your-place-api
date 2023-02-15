from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.dependencies.db import get_db
from app.models.coworking_model import *
from app.schemas.coworking_schema import *
import app.crud.coworking_crud as crud


coworking_router = APIRouter(
    prefix="/coworking",
    tags=['coworking'],
)


@coworking_router.post("/create_coworking", response_model=SchemaCoworking)
def create_coworking(coworking: SchemaCoworkingCreate, db: Session = Depends(get_db)):
    db_coworking = crud.create_coworking(coworking=coworking, db=db)
    return db_coworking


@coworking_router.get("/")
def get_all_coworking(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Coworking).offset(skip).limit(limit).all()