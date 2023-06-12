from uuid import UUID

from app.models.tariff_model import TariffBase


class TarriffCreate(TariffBase):
    pass


class TariffUpdate(TariffBase):
    pass


class TariffRead(TariffBase):
    id: UUID
