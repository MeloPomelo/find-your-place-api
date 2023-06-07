from app.crud.base_crud import CRUDBase
from app.models import Comment
from app.schemas.comment_schema import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    pass


comment = CRUDComment(Comment)