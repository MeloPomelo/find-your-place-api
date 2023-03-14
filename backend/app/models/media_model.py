from app.models.base_model import BaseUUIDModel
from sqlmodel import SQLModel
from typing import Optional


class MediaBase(SQLModel):
    title: Optional[str]
    decription: Optional[str]
    path: Optional[str]


class Media(BaseUUIDModel, MediaBase, table=True):
    pass
