from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, List
from uuid import UUID

from app.models.base_model import BaseUUIDModel
from app.models.workspace_model import WorkspaceParameterLink

class ParameterBase(SQLModel):
    name: str
    code_name: Optional[str]

class Parameter(BaseUUIDModel, ParameterBase, table=True):
    category: Optional["Category"] = Relationship(
        back_populates="parameters", sa_relationship_kwargs={"lazy": "joined"}
    )
    category_id: Optional[UUID] = Field(default=None, foreign_key="Category.id")

    workspaces: List["Workspace"] = Relationship(
        back_populates="parameters", link_model=WorkspaceParameterLink, sa_relationship_kwargs={"lazy": "selectin"}
    )

