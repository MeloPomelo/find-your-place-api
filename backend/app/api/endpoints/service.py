from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import HTTPException
from uuid import UUID
from fastapi_async_sqlalchemy import db

from app.api.endpoints import deps
from app.models.users_model import User
from app.crud.parameter_crud import parameter
from app.crud.category_crud import category
from app.crud.status_crud import status
from app.crud.workspace_crud import workspace

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

router = APIRouter()


@router.get("/parameters")
async def get_parameters_list(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> StreamingResponse:
    parameters = await parameter.get_multi(skip=skip, limit=limit)
    return parameters


@router.get("/categories")
async def get_categories_list(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
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
    code_name: str
) -> PutResponseBase[WorkspaceRead]:
    current_workspace = await workspace.get(id=workspace_id)
    new_status = await status.get_status_by_code_name(code_name=code_name, db_session=db.session)
    if not new_status:
        raise HTTPException(status_code=404, detail="Status not found")
    current_workspace = await workspace.set_status(workspace=current_workspace, status=new_status)
    return create_response(data=current_workspace)