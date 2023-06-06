from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params
from sqlmodel import select
from datetime import timedelta

from app.core import security
from app.core.config import settings
from app.crud import user_crud as crud
from app.crud.workspace_crud import workspace
from app.crud.visit_crud import visit
from app.models.users_model import User
from app.models.workspace_model import Workspace
from app.models import Visit
from app.schemas.response_schemas import GetResponseBase, create_response, GetResponsePaginated
from app.schemas.user_schema import UserCreate, UserRead
from app.schemas.workspace_schema import WorkspaceRead
from app.schemas.visit_schema import VisitRead
from app.schemas.role_schema import RoleEnum
from app.schemas.token_schema import TokenRead

from app.api.endpoints import deps


router = APIRouter()


@router.post("/registartion", status_code=status.HTTP_201_CREATED)
async def registrate_user(
    # new_user: UserCreate = Depends(user_deps.user_exists),
    new_user: UserCreate,
) -> TokenRead:
    """
    Registration for new users
    """
    user = await crud.user.create_user(obj_in=new_user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("")
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
) -> GetResponseBase[UserRead]:
    """
    Gets my user profile information
    """
    return create_response(data=current_user)

@router.get("/workspaces")
async def get_user_workspaces(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user]))
) -> GetResponsePaginated[WorkspaceRead]:
    """
    Gets users workspaces
    """
    workspaces = await workspace.get_multi_paginated(
        params=params, 
        query=select(Workspace).where(Workspace.user_id==current_user.id)
    )
    return create_response(data=workspaces)


@router.get("/visits")
async def get_user_visits(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user]))
) -> GetResponsePaginated[VisitRead]:
    """
    Gets users visits
    """
    visits = await visit.get_multi_paginated(
        params=params, 
        query=select(Visit).where(Visit.user_id==current_user.id)
    )
    return create_response(data=visits)
