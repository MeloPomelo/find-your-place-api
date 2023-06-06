from uuid import UUID

from app.models.visit_model import VisitBase


class VisitCreate(VisitBase):
    workspace_id: UUID


class VisitUpdate(VisitBase):
    pass


class VisitRead(VisitBase):
    id: UUID
    workspace_id: UUID
    user_id: UUID
