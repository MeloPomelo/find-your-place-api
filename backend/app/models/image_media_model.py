from .media_model import Media
from app.models.base_model import BaseUUIDModel
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class ImageMediaBase(SQLModel):
    pass

class ImageMedia(BaseUUIDModel, ImageMediaBase, table=True):
    workspace: Optional["Workspace"] = Relationship(
        back_populates="images", sa_relationship_kwargs={"lazy": "joined"}
    )
    workspace_id: Optional[UUID] = Field(default=None, foreign_key="Workspace.id")
    
    media_id: Optional[UUID] = Field(default=None, foreign_key="Media.id")  
    media: Media = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ImageMedia.media_id==Media.id",
        }
    )