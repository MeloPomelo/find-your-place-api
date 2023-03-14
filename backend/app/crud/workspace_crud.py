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
from app.models.media_model import Media
from app.models.image_media_model import ImageMedia

class CRUDWorkspace(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    async def update_photo(
        self,
        *,
        workspace_id: int,
        image: MediaCreate,
        heigth: int,
        width: int,
        file_format: str,
        db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or db.session
        workspace = super().get(id=workspace_id)
        
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


workspace = CRUDWorkspace(Workspace)