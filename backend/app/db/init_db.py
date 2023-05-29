from typing import Dict, List, Union
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud import role_crud, user_crud, category_crud, parameter_crud, status_crud, workspace_crud
from app.schemas.role_schema import RoleCreate
from app.schemas.category_schema import CategoryCreate
from app.schemas.parameter_schema import ParameterCreate
from app.schemas.status_schema import StatusCreate
from app.schemas.workspace_schema import WorkspaceCreate
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
            username="admin"
        ),
        "role": "admin",
    },
    {
        "data": UserCreateWithRole(
            first_name="User",
            last_name="FastAPI",
            password=settings.FIRST_USER_PASSWORD,
            username="user"
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
            name="душевая комната",
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
        )
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
            name="почасовая оплата",
            code_name="hourly_payment"
        ),
        "category": "Дополнительно"
    }
]


workspaces: List[Dict[str, Union[str, WorkspaceCreate]]] = [
    {
        "data": WorkspaceCreate(
            title = "Коворкинг Пространство+",
            description = "Добро пожаловать в коворкинг Пространство+! У нас собираются творческие и активные люди, чтобы вдохновляться и сотрудничать. Наша современная и стильная обстановка создана для эффективной работы и комфорта. Будь вы фрилансером, предпринимателем или частью небольшой команды, мы предоставляем профессиональное пространство, способствующее развитию и обучению.",
            phone_number = "+7 123-456-7890",
            site_url = "www.prostranstvoplus.ru",
            location_value = "ул. Главная, г. Городово, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Уютный Коворкинг",
            description = "Приходите в наш Уютный Коворкинг и наслаждайтесь комфортом и спокойствием. У нас есть все необходимое для эффективной работы и продуктивности. Приятная атмосфера, отдельные рабочие места, быстрый интернет и прекрасный вид из окна помогут вам достичь успеха в своих проектах.",
            phone_number = "+7 987-654-3210",
            site_url = "www.uyutnykovorking.ru",
            location_value = "пр. Парковый, г. Уютовск, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Идея Хаб",
            description = "Добро пожаловать в Идея Хаб - место, где рождаются идеи! Наш коворкинг предоставляет стимулирующую среду для креативности и инноваций. Современный дизайн, открытые рабочие пространства и возможность общения с единомышленниками сделают вашу работу более интересной и продуктивной.",
            phone_number = "+7 987-654-3211",
            site_url = "www.ideyahub.ru",
            location_value = "ул. Идеальная, г. Новоидейск, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Стартап Центр",
            description = "Стартап Центр - идеальное место для развития вашего стартапа. У нас вы найдете все необходимое для успешного старта и роста вашего бизнеса. Современное оборудование, наставничество от опытных предпринимателей и возможность взаимодействия с другими стартапами создадут идеальную среду для вашего успеха.",
            phone_number = "+7 987-654-3212",
            site_url = "www.startupcenter.ru",
            location_value = "пл. Стартовая, г. Начальноград, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Инновационный Коворкинг",
            description = "Инновационный Коворкинг - место, где современные идеи становятся реальностью. У нас вы сможете работать рядом с другими творческими и профессиональными людьми, которые разделяют вашу страсть к инновациям. Отличные рабочие условия, доступ к новейшим технологиям и оборудованию помогут вам воплотить в жизнь свои самые смелые идеи.",
            phone_number = "+7 987-654-3213",
            site_url = "www.innovacoworking.ru",
            location_value = "ул. Инновационная, г. Прогрессово, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Креативный Хаб",
            description = "Добро пожаловать в Креативный Хаб - место, где идеи становятся реальностью! Наш коворкинг предоставляет вдохновение, свободу и возможности для вашего творчества. Уютная обстановка, современное оборудование и разнообразные мероприятия помогут вам раскрыть свой потенциал и достичь успеха в своей деятельности.",
            phone_number = "+7 987-654-3214",
            site_url = "www.creativehub.ru",
            location_value = "ул. Творческая, г. Идейск, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Совместное Пространство",
            description = "Совместное Пространство - идеальное место для работы и сотрудничества. У нас вы найдете комфортабельные рабочие места, современное оборудование и возможность общения с другими предпринимателями и профессионалами различных отраслей. Здесь вы сможете развивать свои проекты и находить новые возможности для роста.",
            phone_number = "+7 987-654-3215",
            site_url = "www.sovmeshcoworking.ru",
            location_value = "пр. Сотрудничества, г. Совместное, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Технологический Центр",
            description = "Технологический Центр - место, где воплощаются технологические идеи в жизнь. У нас вы найдете современное оборудование, лаборатории, прототипирование и доступ к техническим экспертам. Работая вместе с нами, вы сможете ускорить развитие своих технологических проектов и достичь новых высот.",
            phone_number = "+7 987-654-3216",
            site_url = "www.techhub.ru",
            location_value = "ул. Технологическая, г. Техноград, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Индустриальный Коворкинг",
            description = "Индустриальный Коворкинг - место, где сходятся идеи и технологии. У нас вы найдете просторные рабочие площади, оборудованные мастерские и доступ к специализированным инструментам. Будь вы дизайнером, инженером или изобретателем, мы предоставляем вам все необходимое для реализации ваших проектов.",
            phone_number = "+7 987-654-3217",
            site_url = "www.industriacoworking.ru",
            location_value = "ул. Индустриальная, г. Производск, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        )
    },
    {
        "data": WorkspaceCreate(
            title = "Коворкинг Бизнес-Центр",
            description = "Коворкинг Бизнес-Центр - идеальное место для успешного бизнеса. У нас вы найдете современные офисные пространства, конференц-залы и все необходимое для эффективной работы. Будь вы представителем крупной компании или стартапом, мы поможем вам создать комфортные условия для достижения ваших целей.",
            phone_number = "+7 987-654-3218",
            site_url = "www.bizcentercoworking.ru",
            location_value = "пр. Бизнесовый, г. Бизнесово, Россия",
            longitude = 0,
            latitude = 0,
            images_id = [],
            parameters = []
        ),
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

    user = await user_crud.user.get_by_username(username='admin', db_session=db_session)

    for workspace in workspaces:
        await workspace_crud.workspace.create(obj_in=workspace["data"], user_id=user.id, db_session=db_session)