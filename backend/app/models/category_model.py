from sqlmodel import SQLModel, Relationship
from typing import List, Optional

from app.models.base_model import BaseUUIDModel


class CategoryBase(SQLModel):
    name: str
    code_name: Optional[str]


class Category(BaseUUIDModel, CategoryBase, table=True):
    parameters: List["Parameter"] = Relationship(  # noqa: F821
        back_populates="category", sa_relationship_kwargs={"lazy": "selectin"}
    )