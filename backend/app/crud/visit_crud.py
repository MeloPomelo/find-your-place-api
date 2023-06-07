from app.crud.base_crud import CRUDBase
from app.models import Visit
from app.schemas.visit_schema import VisitCreate, VisitUpdate


class CRUDVisit(CRUDBase[Visit, VisitCreate, VisitUpdate]):
    pass


visit = CRUDVisit(Visit)