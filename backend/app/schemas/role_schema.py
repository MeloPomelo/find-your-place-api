from enum import Enum
from app.models.role_model import RoleBase
from uuid import UUID


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: UUID


class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"