from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.schemas.status_schema import StatusCreate, StatusUpdate
from app.models.status_model import Status
from app.models.workspace_model import Workspace
from app.crud.base_crud import CRUDBase


class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    async def get_status_by_title(
        self,
        *,
        title: str,
        db_session: Optional[AsyncSession] = None
    ) -> Status:
        db_session = db_session or super().get_db().session
        status = await db_session.execute(select(Status).where(Status.title == title))
        return status.scalar_one_or_none()
    
    async def change_workspace_status(
        self,
        *,
        workspace: Workspace,
        status_id: UUID,
        db_session: Optional[AsyncSession] = None
    ) -> Status:
        db_session = super().get_db().session
        workspace.status_id = status_id
        db_session.add(workspace)
        await db_session.commit()
        await db_session.refresh(workspace)
        return workspace
    

status = CRUDStatus(Status)