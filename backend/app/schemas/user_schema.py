from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel
from app.models.users_model import UserBase


'''
 Стандартная реализация
'''

class LoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

class UserCreate(UserBase):
    password: Optional[str]

    class Config:
        hashed_password = None

class UserCreateWithRole(UserBase):
    password: Optional[str]
    role_id: Optional[UUID]

    class Config:
        hashed_password = None

class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True


'''
Для Firebase


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True
'''

        