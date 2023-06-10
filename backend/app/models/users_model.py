from datetime import datetime
from sqlmodel import Field, SQLModel, DateTime, Column, Relationship
from typing import Optional, List
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: Optional[str] = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    phone: Optional[str]
    username: str = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    birthdate: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    bonus_balance: Optional[float] = Field(default=0)


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: Optional[str] = Field(nullable=False, index=True)

    role: Optional["Role"] = Relationship(  # noqa: F821
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )
    role_id: Optional[UUID] = Field(default=None, foreign_key="Role.id")

    workspaces: List["Workspace"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    comments: List["Comment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    visits: List["Visit"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    is_active: bool = Field(default=True)