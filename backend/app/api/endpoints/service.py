from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from uuid import UUID
from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params
from typing import Optional
from sqlmodel import select
from app.api.endpoints import deps
from app.models.users_model import User
from app.models.workspace_model import Workspace
from app.crud.parameter_crud import parameter
from app.crud.category_crud import category
from app.crud.status_crud import status
from app.crud.workspace_crud import workspace
from app.crud.user_crud import user

from app.schemas.response_schemas import (
    GetResponseBase,
    GetResponsePaginated,
    PostResponseBase, 
    PutResponseBase, 
    DeleteResponseBase,
    create_response,
)
from app.schemas.parameter_schema import ParameterRead
from app.schemas.role_schema import RoleEnum
from app.schemas.workspace_schema import WorkspaceRead
from app.schemas.status_schema import IStatusWorkspace


router = APIRouter()


@router.get("/parameters")
async def get_parameters_list(
    skip: int = 0, 
    limit: int = 100,
) -> StreamingResponse:
    parameters = await parameter.get_multi(skip=skip, limit=limit)
    return parameters


@router.get("/categories")
async def get_categories_list(
    skip: int = 0, 
    limit: int = 100,
) -> StreamingResponse:
    categories = await category.get_multi(skip=skip, limit=limit)
    return categories


@router.get("/statuses")
async def get_statuses_list(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> StreamingResponse:
    statuses = await status.get_multi(skip=skip, limit=limit)
    return statuses


@router.put("/set_status")
async def set_workspace_status(
    workspace_id: UUID,
    code_name: Optional[IStatusWorkspace] = Query(
        default=IStatusWorkspace.approved
    ),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> PutResponseBase[WorkspaceRead]:
    current_workspace = await workspace.get(id=workspace_id)
    new_status = await status.get_status_by_code_name(code_name=code_name, db_session=db.session)
    if not new_status:
        raise HTTPException(status_code=404, detail="Status not found")
    current_workspace = await workspace.set_status(workspace=current_workspace, status=new_status)
    await user.add_bonuses(user_id=current_workspace.user_id, amount=50)
    return create_response(data=current_workspace)


@router.get("/workspaces")
async def get_workspace_list(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
    status: Optional[IStatusWorkspace] = Query(default=None)
) -> GetResponsePaginated[WorkspaceRead]:
    """
    Gets a paginated list of workspaces
    """
    query = select(Workspace)
    if status:
        query = query.join(Workspace.status).where(Workspace.status.property.mapper.c.code_name == status)
    workspaces = await workspace.get_multi_paginated(params=params, query=query)
    return create_response(data=workspaces)