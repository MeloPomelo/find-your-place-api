from typing import Dict, List, Union
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud import role_crud, user_crud
from app.schemas.role_schema import RoleCreate
from app.core.config import settings
from app.schemas.user_schema import UserCreate


roles: List[RoleCreate] = [
    RoleCreate(name="admin", description="This the Admin role"),
    RoleCreate(name="manager", description="Manager role"),
    RoleCreate(name="user", description="User role"),
]


users: List[Dict[str, Union[str, UserCreate]]] = [
    {
        "data": UserCreate(
            first_name="Admin",
            last_name="FastAPI",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username="admin"
        ),
        "role": "admin",
    },
    {
        "data": UserCreate(
            first_name="User",
            last_name="FastAPI",
            password=settings.FIRST_USER_PASSWORD,
            username="user"
        ),
        "role": "user",
    },
]


async def init_db(db_session: AsyncSession) -> None:

    for role in roles:
        role_current = await role_crud.role.get_role_by_name(
            name=role.name, db_session=db_session
        )
        if not role_current:
            await role_crud.role.create(obj_in=role, db_session=db_session)

    for user in users:
        current_user = await user_crud.user.get_by_username(
            username=user["data"].username, db_session=db_session
        )
        role = await role_crud.role.get_role_by_name(
            name=user["role"], db_session=db_session
        )
        if not current_user:
            user["data"].role_id = role.id
            await user_crud.user.create_user(obj_in=user["data"], db_session=db_session)

   

   