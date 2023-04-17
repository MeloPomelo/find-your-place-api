from sqlmodel import SQLModel, Relationship
from typing import List

from app.models.base_model import BaseUUIDModel


class CategoryBase(SQLModel):
    title: str


class Category(BaseUUIDModel, CategoryBase, table=True):
    parameters: List["Parameter"] = Relationship(  # noqa: F821
        back_populates="category", sa_relationship_kwargs={"lazy": "selectin"}
    )