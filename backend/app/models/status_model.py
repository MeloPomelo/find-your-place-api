from sqlmodel import SQLModel, Relationship
from typing import List

from app.models.base_model import BaseUUIDModel


class StatusBase(SQLModel):
    title: str
    tag: str


class Status(BaseUUIDModel, StatusBase, table=True):
    workspaces: List["Workspace"] = Relationship(
        back_populates="status", sa_relationship_kwargs={"lazy": "selectin"}
    )