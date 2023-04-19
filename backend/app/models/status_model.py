from sqlmodel import SQLModel, Relationship
from typing import List, Optional

from app.models.base_model import BaseUUIDModel


class StatusBase(SQLModel):
    name: str
    code_name: Optional[str]
    tag: str


class Status(BaseUUIDModel, StatusBase, table=True):
    workspaces: List["Workspace"] = Relationship(
        back_populates="status", sa_relationship_kwargs={"lazy": "selectin"}
    )