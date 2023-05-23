from app.models.status_model import StatusBase
from uuid import UUID
from enum import Enum

class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusRead(StatusBase):
    id: UUID


class IStatusWorkspace(str, Enum):
    handling = 'handling'
    canceled = 'canceled'
    approved = 'approved'
