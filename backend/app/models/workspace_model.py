from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime

from typing import List, Optional
from pydantic import EmailStr
from app.models.base_model import BaseUUIDModel


class WorkspaceBase(SQLModel):
    title: Optional[str] = Field(nullable=False)
    description: Optional[str] = Field(nullable=False)

class Workspace(BaseUUIDModel, WorkspaceBase,table=True):
    __tablename__ = "workspaces"
    pass


