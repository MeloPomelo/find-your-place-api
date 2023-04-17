from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.schemas.role_schema import RoleCreate, RoleUpdate
from app.models.role_model import Role
from app.models.users_model import User
from app.crud.base_crud import CRUDBase


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    async def get_role_by_name(
        self, *, name: str, db_session: Optional[AsyncSession] = None
    ) -> Role:
        db_session = db_session or super().get_db().session
        role = await db_session.execute(select(Role).where(Role.name == name))
        return role.scalar_one_or_none()

    async def add_role_to_user(self, *, user: User, role_id: UUID) -> Role:
        db_session = super().get_db().session
        role = await super().get(id=role_id)
        role.users.append(user)
        db_session.add(role)
        await db_session.commit()
        await db_session.refresh(role)
        return role


role = CRUDRole(Role)