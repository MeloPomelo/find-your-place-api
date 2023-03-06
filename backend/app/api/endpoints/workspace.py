from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination import Params

from app.api.endpoints import deps
from app.models.users_model import User
from app.crud import workspace_crud as crud 
from app.models.workspace_model import Workspace
from app.schemas.role_schema import RoleEnum
from app.schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceRead,
    WorkspaceUpdate,
)
from app.schemas.response_schemas import (
    GetResponseBase,
    GetResponsePaginated,
    PostResponseBase, 
    PutResponseBase, 
    DeleteResponseBase,
    create_response,
)


router = APIRouter()


@router.get("")
async def get_workspace_list(
    params: Params = Depends(),
) -> GetResponsePaginated[WorkspaceRead]:
    """
    Gets a paginated list of workspaces
    """
    workspaces = await crud.workspace.get_multi_paginated(params=params)
    return create_response(data=workspaces)



@router.get("/{workspace_id}")
async def get_workspace_by_id(
    workspace_id: UUID,
) -> GetResponseBase[WorkspaceRead]:
    """
    Gets a workspace by its id
    """
    workspace = await crud.workspace.get(id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return create_response(data=workspace)


@router.post("/create_workspace")
async def create_workspace(
    workspace: WorkspaceCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> PostResponseBase[WorkspaceRead]:
    """
    Create a new workspace
    """
    workspace = await crud.workspace.create(obj_in=workspace)
    return create_response(data=workspace)


@router.put("/update_workspace")
async def update_workspace(
    workspace_id: UUID,
    workspace: WorkspaceUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> PutResponseBase[WorkspaceUpdate]:
    """
    Upadate a workspace
    """
    current_workspace = await crud.workspace.get(id=workspace_id)
    if not current_workspace:
        raise HTTPException(status_code=404, detail="Worksapce not found")
    workspace_updated = await crud.workspace.update(obj_new=workspace, obj_current=current_workspace)
    return create_response(data=workspace_updated)


@router.delete("/delete_workspace")
async def delete_workspace(
    workspace_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> DeleteResponseBase[WorkspaceRead]:
    """
    Delete a workspace
    """
    current_workspace = await crud.workspace.get(id=workspace_id)
    if not current_workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    workspace = await crud.workspace.remove(id=workspace_id)
    return create_response(workspace)