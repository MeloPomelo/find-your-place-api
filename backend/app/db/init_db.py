from typing import Dict, List, Union
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud import role_crud, user_crud, category_crud, parameter_crud, status_crud
from app.schemas.role_schema import RoleCreate
from app.schemas.category_schema import CategoryCreate
from app.schemas.parameter_schema import ParameterCreate
from app.schemas.status_schema import StatusCreate
from app.core.config import settings
from app.schemas.user_schema import UserCreateWithRole


roles: List[RoleCreate] = [
    RoleCreate(name="admin", description="This the Admin role"),
    RoleCreate(name="manager", description="Manager role"),
    RoleCreate(name="user", description="User role"),
]


users: List[Dict[str, Union[str, UserCreateWithRole]]] = [
    {
        "data": UserCreateWithRole(
            first_name="Admin",
            last_name="FastAPI",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username="admin",
            bonus_balance=0,
        ),
        "role": "admin",
    },
    {
        "data": UserCreateWithRole(
            first_name="User",
            last_name="FastAPI",
            password=settings.FIRST_USER_PASSWORD,
            username="user",
            bonus_balance=0,
        ),
        "role": "user",
    },
]

categories: List[CategoryCreate] = [
    CategoryCreate(name="Комнаты"),
    CategoryCreate(name="Дополнительно"),
    CategoryCreate(name="Технические особенности"),
]


statuses: List[StatusCreate] = [
    StatusCreate(
        name="Обработка формы", 
        code_name="handling", 
        tag="workspace_status",
    ),
    StatusCreate(
        name="Форма отклонена", 
        code_name="canceled", 
        tag="workspace_status",
    ),
    StatusCreate(
        name="Подтверждено", 
        code_name="approved", 
        tag="workspace_status",
    ),
    StatusCreate(
        name="Прошедшее",
        code_name="not active", 
        tag="visit_status",
    ),
    StatusCreate(
        name="Активное", 
        code_name="active", 
        tag="visit_status",
    ),
    StatusCreate(
        name="Предстоящее",
        code_name="future",  
        tag="visit_status",
    ),
]


parameters: List[Dict[str, Union[str, ParameterCreate]]] = [
    {
        "data": ParameterCreate(
            name="Печать материалов",
            code_name="print"
        ),
        "category": "Технические особенности",
    },
    {
        "data": ParameterCreate(
            name="Wi-Fi",
            code_name="wifi"
        ),
        "category": "Технические особенности"
    },
    {
        "data": ParameterCreate(
            name="Конференц зал",
            code_name="podium"
        ),
        "category": "Комнаты"
    },
    {
        "data": ParameterCreate(
            name="Душевая комната",
            code_name="shower"
        ),
        "category": "Комнаты"
    },
    {
        "data": ParameterCreate(
            name="Комната переговоров",
            code_name="meeting_room"
        ),
        "category": "Комнаты"
    },
    {
        "data": ParameterCreate(
            name="Комната для курения",
            code_name="smoking_rooms"
        ),
        "category": "Комнаты"
    },
    {
        "data": ParameterCreate(
            name="Чай, Кофе",
            code_name="local_cafe"
        ),
        "category": "Дополнительно"
    },
    {
        "data": ParameterCreate(
            name="Круглосуточно",
            code_name="24mp"
        ),
        "category": "Дополнительно"
    },
    {
        "data": ParameterCreate(
            name="Метро",
            code_name="subway"
        ),
        "category": "Дополнительно"
    },
    {
        "data": ParameterCreate(
            name="Аренда гаджетов",
            code_name="keyboard"
        ),
        "category": "Дополнительно"
    },
    {
        "data": ParameterCreate(
            name="Почасовая оплата",
            code_name="paid"
        ),
        "category": "Дополнительно"
    }
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
            await user_crud.user.create_with_role(obj_in=user["data"], db_session=db_session)

    for category in categories:
        category_current = await category_crud.category.get_category_by_name(
            name=category.name, db_session=db_session
        )
        if not category_current:
            await category_crud.category.create(obj_in=category, db_session=db_session)
   

    for parameter in parameters:
        parameter_current = await parameter_crud.parameter.get_parameter_by_name(
            name=parameter["data"].name, db_session=db_session
        )
        category = await category_crud.category.get_category_by_name(
            name=parameter["category"], db_session=db_session
        )
        if not parameter_current:
            parameter["data"].category_id = category.id
            await parameter_crud.parameter.create(obj_in=parameter["data"], db_session=db_session)

    for status in statuses:
        status_current = await status_crud.status.get_status_by_code_name(
            code_name=status.code_name, db_session=db_session
        )
        if not status_current:
            await status_crud.status.create(obj_in=status, db_session=db_session)
