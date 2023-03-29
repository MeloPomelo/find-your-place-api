from uuid import UUID
from typing import Optional, List
from datetime import datetime
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.workspace_model import Workspace
from app.models.comment_model import Comment
from app.schemas.workspace_schema import WorkspaceCreate, WorkspaceUpdate
from app.schemas.comment_schema import CommentCreate
from app.crud.base_crud import CRUDBase
from app.crud.image_media_crud import image_media


class CRUDWorkspace(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    async def add_image_to_workspace(
            self,
            *,
            workspace_id: int,
            image_id: int,
            db_session: Optional[AsyncSession] = None
    ):
        db_session = db_session or db.session

        db_image = await image_media.get(id=image_id)
        db_image.workspace_id = workspace_id
        db_session.add(db_image)
        await db_session.commit()
        await db_session.refresh(db_image)


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