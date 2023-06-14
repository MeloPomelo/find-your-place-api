from uuid import UUID
from typing import Optional, List
from datetime import datetime
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.workspace_model import Workspace
from app.models.media_model import Media
from app.models.image_media_model import ImageMedia
from app.schemas.media_schema import MediaCreate
from app.schemas.image_media_schema import ImageMediaCreate, ImageMediaUpdate
from app.crud.base_crud import CRUDBase


class CRUDImageMedia(CRUDBase[ImageMedia, ImageMediaCreate, ImageMediaUpdate]):
    async def upload_image(
            self,
            *,
            image: MediaCreate,
            db_session: Optional[AsyncSession] = None
    ) -> Workspace:
        db_session = db_session or super().get_db().session

        image_media = ImageMedia(
            media=Media.from_orm(image),
        )
        db_session.add(image_media)
        await db_session.commit()
        await db_session.refresh(image_media)
        return image_media
    
    
image_media = CRUDImageMedia(ImageMedia)