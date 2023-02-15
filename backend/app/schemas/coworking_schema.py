from uuid import uuid4, UUID
from pydantic import BaseModel, Field


class CoworkingBase(BaseModel):
    title: str
    description: str


class SchemaCoworkingCreate(CoworkingBase):
    pass


class SchemaCoworkingUpdate(CoworkingBase):
    pass


class SchemaCoworking(CoworkingBase):
    # uuid: UUID = Field(default_factory=uuid4)
    id: int

    class Config:
        orm_mode = True

