from uuid import UUID
from typing import List, Optional

from app.models.workspace_model import WorkspaceBase
from app.schemas.image_media_schema import ImageMediaRead
from app.schemas.comment_schema import CommentRead
from app.schemas.parameter_schema import ParameterRead
from app.schemas.status_schema import StatusRead
from app.schemas.tariff_schema import TariffRead, TarriffCreate


class WorkspaceCreate(WorkspaceBase):
    images_id: Optional[List[UUID]] = []
    parameters: Optional[List[str]] = []
    tariffs: Optional[List[TarriffCreate]] = []

class WorkspaceUpdate(WorkspaceBase):
    images_id: Optional[List[UUID]] = []
    parameters: Optional[List[str]] = []


class WorkspaceRead(WorkspaceBase):
    id: UUID
    user_id: UUID
    status: Optional[StatusRead]
    rating: int
    images:  Optional[List[ImageMediaRead]] = []
    comments: Optional[List[CommentRead]] = []
    parameters: Optional[List[ParameterRead]] = []
    tariffs: Optional[List[TariffRead]] = []


class WorkspaceDelete(WorkspaceBase):
    id: UUID
    user_id: UUID