from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime
from typing import List, Optional
from pydantic import EmailStr
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class WorkspaceBase(SQLModel):
    title: Optional[str] = Field(nullable=False)
    description: Optional[str] = Field(nullable=False)
    phone_number: Optional[str]
    site_url: Optional[str]
    location_value: Optional[str] = Field(nullable=False)
    longitude: Optional[float] = Field(nullable=False)
    latitude: Optional[float] = Field(nullable=False)


class WorkspaceParameterLink(BaseUUIDModel, table=True):
    workspace_id: Optional[UUID] = Field(
        default=None, foreign_key="Workspace.id", primary_key=True
    ) 

    parameter_id: Optional[UUID] = Field(
        default=None, foreign_key="Parameter.id", primary_key=True
    )

class Workspace(BaseUUIDModel, WorkspaceBase, table=True):  
    rating: Optional[float] = Field(nullable=False, default=0)
    sum_rating: Optional[int] = Field(nullable=False, default=0)

    status: Optional["Status"] = Relationship(
        back_populates="workspaces", sa_relationship_kwargs={"lazy": "joined"}
    )
    status_id: Optional[UUID] = Field(default=None, foreign_key="Status.id")

    user: Optional["User"] = Relationship(
        back_populates="workspaces", sa_relationship_kwargs={"lazy": "joined"}
    )
    user_id: Optional[UUID] = Field(default=None, foreign_key="User.id")

    images: List["ImageMedia"] = Relationship(  # noqa: F821
        back_populates="workspace", sa_relationship_kwargs={"lazy": "selectin"}
    )

    comments: List["Comment"] = Relationship(
        back_populates="workspace", sa_relationship_kwargs={"lazy": "selectin"}
    )

    visits: List["Visit"] = Relationship(
       back_populates="workspace", sa_relationship_kwargs={"lazy": "selectin"}
    )

    parameters: List["Parameter"] = Relationship(
        back_populates="workspaces", link_model=WorkspaceParameterLink, sa_relationship_kwargs={"lazy": "selectin"}
    ) 

    

