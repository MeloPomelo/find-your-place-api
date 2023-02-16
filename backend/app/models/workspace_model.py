from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime

from typing import List, Optional
from pydantic import EmailStr
from app.models.base_model import BaseUUIDModel


class Workspace(BaseUUIDModel, table=True):
    title: Optional[str] = Field(nullable=False)
    description: Optional[str] = Field(nullable=False)


