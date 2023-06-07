from uuid import UUID
from sqlmodel import Field, Relationship, column, SQLModel
from typing import Optional, List
from datetime import datetime

from app.models.base_model import BaseUUIDModel


class TariffBase(SQLModel):
    title: str
    interval: str
    cost: float


class Tariff(BaseUUIDModel, TariffBase, table=True):
    workspace: Optional["Workspace"] = Relationship(
        back_populates="tariffs", sa_relationship_kwargs={"lazy": "joined"}
    )
    workspace_id: Optional[UUID] = Field(default=None, foreign_key="Workspace.id")

    visits: List["Visit"] = Relationship(
        back_populates="tariff", sa_relationship_kwargs={"lazy": "selectin"}
    )