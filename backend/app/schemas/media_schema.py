from app.utils.minio_client import MinioClient
from app.models.media_model import MediaBase
from pydantic import validator, AnyHttpUrl
from app.core.config import settings
from app import api
from typing import Any, Optional, Union
from uuid import UUID
from app.api.endpoints.deps import minio_auth

class MediaCreate(MediaBase):
    pass


class MediaUpdate(MediaBase):
    pass


class MediaRead(MediaBase):
    id: Union[UUID, str]
    link: Optional[str] = None

    @validator(
        "link", pre=True, check_fields=False, always=True
    )  # Always true because link does not exist in the database
    def default_icon(cls, value: Any, values: Any) -> AnyHttpUrl:
        if values["path"] is None:
            return ""
        minio: MinioClient = minio_auth()
        url = minio.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET, object_name=values["path"]
        )
        return url