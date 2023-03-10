
from app.models.image_media_model import ImageMediaBase
from app.schemas.media_schema import MediaRead
from typing import Optional


class ImageMediaCreate(ImageMediaBase):
    pass


class ImageMediaUpdate(ImageMediaBase):
    pass


class ImageMediaRead(ImageMediaBase):
    media: Optional[MediaRead]