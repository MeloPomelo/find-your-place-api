from uuid import UUID
from typing import List, Optional

from app.models.workspace_model import WorkspaceBase
from app.schemas.image_media_schema import ImageMediaRead

class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    id: UUID
    images:  Optional[List[ImageMediaRead]] = []

    class Config:
        orm_mode = True
    

