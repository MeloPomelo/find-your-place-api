from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import HTTPException
from uuid import UUID

from app.api.endpoints import deps
from app.models.users_model import User
from app.crud.parameter_crud import parameter
from app.crud.category_crud import category
from app.crud.status_crud import status

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