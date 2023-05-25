from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.schemas.parameter_schema import ParameterCreate, ParameterUpdate
from app.models.parameter_model import Parameter
from app.crud.base_crud import CRUDBase


class CRUDParameter(CRUDBase[Parameter, ParameterCreate, ParameterUpdate]):
    async def get_parameter_by_name(
        self, *, name: str, db_session: Optional[AsyncSession] = None
    ) -> Parameter:
        db_session = db_session or super().get_db().session
        parameter = await db_session.execute(select(Parameter).where(Parameter.name == name))
        return parameter.scalar_one_or_none()
    

    async def get_parameter_by_code_name(
        self, *, code_name: str, db_session: Optional[AsyncSession] = None
    ) -> Parameter:
        db_session = db_session or super().get_db().session
        parameter = await db_session.execute(select(Parameter).where(Parameter.code_name == code_name))
        return parameter.scalar_one_or_none()


parameter = CRUDParameter(Parameter)