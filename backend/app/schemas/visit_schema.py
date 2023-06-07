from uuid import UUID

from app.models.visit_model import VisitBase


class VisitCreate(VisitBase):
    workspace_id: UUID
    tariff_id: UUID

class VisitUpdate(VisitBase):
    pass


class VisitRead(VisitBase):
    id: UUID
    user_id: UUID
    workspace_id: UUID
    tariff_id: UUID
