from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime
from typing import List, Optional
from pydantic import EmailStr
from uuid import UUID

from app.models.base_model import BaseUUIDModel
from .dictionary_model import Dictionary


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

    parameters: List["WorkspaceParameters"] = Relationship(
        back_populates="workspace", sa_relationship_kwargs={"lazy": "selectin"}
    ) 


class WorkspaceParameters(BaseUUIDModel, table=True):
    workspace: Optional["Workspace"] = Relationship(
        back_populates="parameters", sa_relationship_kwargs={"lazy": "joined"}
    )

    workspace_id: Optional[UUID] = Field(
        default=None, foreign_key="Workspace.id", primary_key=True
    ) 

    parameter: Optional["Parameter"] = Relationship(
        back_populates="workspaces", sa_relationship_kwargs={"lazy": "joined"}
    )

    parameter_id: Optional[UUID] = Field(
        default=None, foreign_key="Parameter.id", primary_key=True
    )
