from uuid import UUID
from datetime import datetime

from app.models.comment_model import CommentBase


class CommentCreate(CommentBase):
    workspace_id: UUID

class CommentUpdate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: UUID
    user_id: UUID
    created_at: datetime
