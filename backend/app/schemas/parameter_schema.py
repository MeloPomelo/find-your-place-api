from uuid import UUID
from typing import Optional
from app.models.parameter_model import ParameterBase
from enum import Enum

class ParameterCreate(ParameterBase):
    category_id: Optional[UUID]


class ParameterUpdate(ParameterBase):
    pass


class ParameterRead(ParameterBase):
    id: UUID


class IParametersRooms(str, Enum):
    meeting = 'meeting_room'
    conference = 'conference_room'
    shower = 'shower_room'


class IParametersFeatures(str, Enum):
    printer = 'printer'
    wi_fi = 'wi-fi'


class IParametersAdditional(str, Enum):
    service = 'service'
    _24hours = '24/7'
    gadget_rental = 'gadget_rental'
    hourly_payment = 'hourly_payment'
