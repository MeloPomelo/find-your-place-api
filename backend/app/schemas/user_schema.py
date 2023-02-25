from uuid import UUID
from pydantic import BaseModel 


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True
        