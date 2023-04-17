from uuid import UUID
from typing import List, Optional

from app.models.category_model import CategoryBase
from app.schemas.parameter_schema import ParameterRead


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID
    # parameters: Optional[List[ParameterRead]] = []