from uuid import UUID

from app.models.comment_model import CommentBase


class CommentCreate(CommentBase):
    workspace_id: UUID

class CommentUpdate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: UUID
    workspace_id: UUID
    user_id: UUID
