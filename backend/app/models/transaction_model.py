from datetime import datetime
from sqlmodel import Field, SQLModel, DateTime, Column, Relationship
from typing import Optional, List
from uuid import UUID


from app.models.base_model import BaseUUIDModel


class TransactionBase(SQLModel):
    amount: int
    description: str


class Transaction(BaseUUIDModel, TransactionBase, table=True):
    user: Optional["User"] = Relationship(
        back_populates="transactions", sa_relationship_kwargs={"lazy": "joined"}
    )
    user_id: Optional[UUID] = Field(default=None, foreign_key="User.id")