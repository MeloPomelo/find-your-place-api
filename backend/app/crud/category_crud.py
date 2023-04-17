from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.crud.base_crud import CRUDBase
from app.models.category_model import Category
from app.models.parameter_model import Parameter
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_category_by_name(
        self, *, title: str, db_session: Optional[AsyncSession] = None
    ) -> Category:
        db_session = db_session or super().get_db().session
        role = await db_session.execute(select(Category).where(Category.title == title))
        return role.scalar_one_or_none()

    async def add_category_to_parameter(self, *, parameter: Parameter, category_id: UUID) -> Category:
        db_session = super().get_db().session
        category = await super().get(id=category_id)
        category.parameters.append(parameter)
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        return category


category = CRUDCategory(Category)