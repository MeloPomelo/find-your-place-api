from uuid import UUID
from sqlmodel import Field, Relationship, column, SQLModel
from typing import Optional, List
from datetime import datetime

from app.models.base_model import BaseUUIDModel


class VisitBase(SQLModel):
    # start_date: datetime
    # end_date: datetime

    start_date: Optional[datetime] = Field(
        default_factory=datetime.utcnow
    )

    end_date: Optional[datetime] = Field(
        default_factory=datetime.utcnow
    )



class Visit(BaseUUIDModel, VisitBase, table=True):
    user: Optional["User"] = Relationship(
        back_populates="visits", sa_relationship_kwargs={"lazy": "joined"}
    )
    user_id: Optional[UUID] = Field(default=None, foreign_key="User.id")

    workspace: Optional["Workspace"] = Relationship(
        back_populates="visits", sa_relationship_kwargs={"lazy": "joined"}
    )
    workspace_id: Optional[UUID] = Field(default=None, foreign_key="Workspace.id")
