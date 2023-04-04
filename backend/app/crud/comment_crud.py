from uuid import UUID
from typing import Optional, List
from datetime import datetime
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.workspace_model import Workspace
from app.models.comment_model import Comment
from app.schemas.workspace_schema import WorkspaceCreate, WorkspaceUpdate
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.crud.base_crud import CRUDBase
from app.crud.image_media_crud import image_media


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    pass


comment = CRUDComment(Comment)