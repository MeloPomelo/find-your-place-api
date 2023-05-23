from uuid import UUID
from typing import Optional, List, Union
from datetime import datetime
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Workspace, Parameter, Status
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
    ) -> Workspace:
        db_session = db_session or db.session
        db_image = await image_media.get(id=image_id)
        workspace.images.append(db_image)
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace
    

    async def remove_image_from_workspace(
        self,
        *,
        workspace: Workspace,
        image_id: int,
        db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or db.session
        db_image = await image_media.get(id=image_id)
        workspace.images.remove(db_image)
        db_session.add(workspace)
        await image_media.remove(id=image_id)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace


    async def add_parameter_to_workspace(
        self,
        *,
        workspace: Workspace,
        parameter: Parameter,
        db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or db.session
        workspace.parameters.append(parameter)
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace


    async def remove_parameter_from_workspace(
        self,
        *,
        workspace: Workspace,
        parameter: Parameter,
        db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or db.session
        workspace.parameters.remove(parameter)
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace


    async def set_status(
        self,
        *,
        workspace: Workspace,
        status: Status,
        db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or db.session
        workspace.status_id = status.id
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace


    async def rating_calculation(
        self,
        *,
        workspace_id: UUID,
        rating: int,
        flag: bool = True,
        db_session: Optional[AsyncSession] = None
    ):
        # Требует доработки
        db_session = db_session or db.session
        curr_workspace = await self.get(id=workspace_id)
        if flag:
            curr_workspace.sum_rating += rating
            curr_workspace.rating = round(curr_workspace.sum_rating / (len(curr_workspace.comments) + 1), 1)
        else:
            curr_workspace.sum_rating -= rating
            if len(curr_workspace.comments) == 1:
                curr_workspace.rating = 0
            else:
                curr_workspace.rating = round(curr_workspace.sum_rating / (len(curr_workspace.comments) - 1), 1)        
        db_session.add(curr_workspace)
        await db_session.commit()
        await db_session.refresh(curr_workspace)


workspace = CRUDWorkspace(Workspace)