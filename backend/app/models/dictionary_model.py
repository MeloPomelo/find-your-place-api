from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime
from typing import List, Optional
from pydantic import EmailStr
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class DictionaryBase(SQLModel):
    code: Optional[str] = Field(nullable=False)
    name: Optional[str] = Field(nullable=False)


class Dictionary(BaseUUIDModel, DictionaryBase, table=True):
    category_id: Optional[UUID] = Field(default=None)
    icon_link: Optional[str] = Field(nullable=True)
    sort_order: Optional[int] = Field(nullable=True)
    number_value: Optional[int] = Field(nullable=True)