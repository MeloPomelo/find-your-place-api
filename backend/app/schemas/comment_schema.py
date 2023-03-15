from uuid import UUID
from typing import List, Optional

from app.models.comment_model import CommentBase
from app.schemas.image_media_schema import ImageMediaRead


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: UUID
