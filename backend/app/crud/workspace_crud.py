from typing import Optional
from app.schemas.workspace_schema import WorkspaceCreate, WorkspaceUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.workspace_model import Workspace
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.media_schema import (
    MediaCreate
)
from app.schemas.comment_schema import (
    CommentCreate
)
from app.models.media_model import Media
from app.models.image_media_model import ImageMedia
from app.models.comment_model import Comment

class CRUDWorkspace(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    async def add_photo(
        self,
        *,
        workspace_id: Optional[int] = None,

        image: MediaCreate,
        heigth: int,
        width: int,
        file_format: str,
        db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or db.session

        image_media = ImageMedia(
            media=Media.from_orm(image),
            workspace_id=workspace_id,
            height=heigth,
            width=width,
            file_format=file_format,
        )
        db_session.add(image_media)
        await db_session.commit()
        await db_session.refresh(image_media)
        return image_media


    async def add_comment(
        self,
        *,
        workspace_id: int,  
        user_id: int,
        comment: CommentCreate,
        db_session: Optional[AsyncSession] = None
    ):
        db_session = db_session or db.session

        db_comment = Comment (
            user_id=user_id,
            workspace_id=workspace_id,
            text=comment.text,
            advantages=comment.advantages,
            disadnatages=comment.disadnatages,
            rating=comment.rating
        )
        db_session.add(db_comment)
        await db_session.commit()
        await db_session.refresh(db_comment)
        return db_comment

workspace = CRUDWorkspace(Workspace)