from datetime import datetime
from sqlmodel import Field, SQLModel, DateTime, Column, Relationship
from typing import Optional, List
from pydantic import EmailStr
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    username: str = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    birthdate: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: Optional[str] = Field(nullable=False, index=True)

    role: Optional["Role"] = Relationship(  # noqa: F821
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )
    role_id: Optional[UUID] = Field(default=None, foreign_key="Role.id")

    comments: List["Comment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    is_active: bool = Field(default=True)