from app.models.image_media_model import ImageMediaBase
from app.schemas.media_schema import MediaRead
from typing import Optional
from uuid import UUID


class ImageMediaCreate(ImageMediaBase):
    id: UUID
    media: Optional[MediaRead]


class ImageMediaUpdate(ImageMediaBase):
    pass


class ImageMediaRead(ImageMediaBase):
    id: UUID
    media: Optional[MediaRead]