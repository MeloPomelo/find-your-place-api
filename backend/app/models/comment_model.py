from uuid import UUID
from sqlmodel import Field, Relationship, column, SQLModel
from typing import Optional, List

from app.models.base_model import BaseUUIDModel


class CommentBase(SQLModel):
    text: str
    advantages: str
    disadnatages: str
    rating: Optional[int] = Field(nullable=False)
    

class Comment(BaseUUIDModel, CommentBase, table=True):
    user: Optional["User"] = Relationship(
        back_populates="comments", sa_relationship_kwargs={"lazy": "joined"}
    )
    user_id: Optional[UUID] = Field(default=None, foreign_key="User.id")

    workspace: Optional["Workspace"] = Relationship(
        back_populates="comments", sa_relationship_kwargs={"lazy": "joined"}
    )
    workspace_id: Optional[UUID] = Field(default=None, foreign_key="Workspace.id")

