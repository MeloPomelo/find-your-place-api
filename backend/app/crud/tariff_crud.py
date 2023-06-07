from app.crud.base_crud import CRUDBase
from app.models import Tariff
from app.schemas.tariff_schema import TarriffCreate, TariffUpdate


class CRUDTariff(CRUDBase[Tariff, TarriffCreate, TariffUpdate]):
    pass


tariff = CRUDTariff(Tariff)