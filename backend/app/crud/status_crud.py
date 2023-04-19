from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.schemas.status_schema import StatusCreate, StatusUpdate
from app.models.status_model import Status
from app.models.workspace_model import Workspace
from app.crud.base_crud import CRUDBase


class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    async def get_status_by_code_name(
        self,
        *,
        code_name: str,
        db_session: Optional[AsyncSession] = None
    ) -> Status:
        db_session = db_session or super().get_db().session
        status = await db_session.execute(select(Status).where(Status.code_name == code_name))
        return status.scalar_one_or_none()
    

status = CRUDStatus(Status)