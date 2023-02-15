from sqlalchemy.orm import Session

from app.models.coworking_model import Coworking as ModelCoworking
from app.schemas.coworking_schema import *

def create_coworking(db: Session, coworking: SchemaCoworkingCreate):
    db_coworking = ModelCoworking(title=coworking.title, description=coworking.description)
    db.add(db_coworking)
    db.commit()
    db.refresh(db_coworking)
    
    return db_coworking