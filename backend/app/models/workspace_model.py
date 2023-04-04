from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime
from typing import List, Optional
from pydantic import EmailStr
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class WorkspaceBase(SQLModel):
    title: Optional[str] = Field(nullable=False)
    description: Optional[str] = Field(nullable=False)
    location_value: Optional[str] = Field(nullable=False)
    longtitude: Optional[float] = Field(nullable=False)
    latitude: Optional[float] = Field(nullable=False)


class Workspace(BaseUUIDModel, WorkspaceBase, table=True):    
    images: List["ImageMedia"] = Relationship(  # noqa: F821
        back_populates="workspace", sa_relationship_kwargs={"lazy": "selectin"}
    )

    comments: List["Comment"] = Relationship(
        back_populates="workspace", sa_relationship_kwargs={"lazy": "selectin"}
    )
