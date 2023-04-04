from typing import Optional
from app.schemas.dictionary_schema import DictionaryCreate, DictionaryUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.dictionary_model import Dictionary
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

class CRUDDictionary(CRUDBase[Dictionary, DictionaryCreate, DictionaryUpdate]):
    pass


dictionary = CRUDDictionary(Dictionary)