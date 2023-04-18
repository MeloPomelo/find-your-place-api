from uuid import UUID
from typing import Optional, List
from datetime import datetime
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.workspace_model import Workspace
from app.models.comment_model import Comment
from app.models.parameter_model import Parameter
from app.schemas.workspace_schema import WorkspaceCreate, WorkspaceUpdate
from app.schemas.comment_schema import CommentCreate
from app.crud.base_crud import CRUDBase
from app.crud.parameter_crud import parameter
from app.crud.image_media_crud import image_media


class CRUDWorkspace(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    async def add_image_to_workspace(
        self,
        *,
        workspace: Workspace,
        image_id: int,
        db_session: Optional[AsyncSession] = None
    ):
        db_session = db_session or db.session
        db_image = await image_media.get(id=image_id)
        workspace.images.append(db_image)
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace
    
    async def add_parameters_to_workspace(
        self,
        *,
        workspace: Workspace,
        parameter: Parameter,
        db_session: Optional[AsyncSession] = None
    ):
        db_session = db_session or db.session
        workspace.parameters.append(parameter)
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace


workspace = CRUDWorkspace(Workspace)