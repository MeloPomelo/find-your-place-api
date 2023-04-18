from app.models.status_model import StatusBase
from uuid import UUID


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusRead(StatusBase):
    id: UUID