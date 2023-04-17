from uuid import UUID
from typing import Optional
from app.models.parameter_model import ParameterBase


class ParameterCreate(ParameterBase):
    category_id: Optional[UUID]


class ParameterUpdate(ParameterBase):
    pass


class ParameterRead(ParameterBase):
    id: UUID