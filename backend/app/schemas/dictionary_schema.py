from uuid import UUID
from typing import List, Optional, Any
from pydantic import validator
from app.models.dictionary_model import DictionaryBase


class DictionaryCreate(DictionaryBase):
    pass

class DictionaryUpdate(DictionaryBase):
    pass


class DictionaryRead(DictionaryBase):
    id: UUID
    category_id: Optional[UUID] = None
    icon_link: Optional[str] = None
    sort_order: Optional[int] = None
    number_value: Optional[int] = None