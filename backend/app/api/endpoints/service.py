from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import HTTPException
from uuid import UUID

from app.crud.parameter_crud import parameter
from app.crud.category_crud import category

from app.schemas.response_schemas import (
    GetResponseBase,
    GetResponsePaginated,
    PostResponseBase, 
    PutResponseBase, 
    DeleteResponseBase,
    create_response,
)
from app.schemas.parameter_schema import ParameterRead

router = APIRouter()


@router.get("/get_parameters")
async def get_parameters_list(skip: int = 0, limit: int = 100) -> StreamingResponse:
    parameters = await parameter.get_multi(skip=skip, limit=limit)
    return parameters


@router.get("/get_categories")
async def get_categories_list(skip: int = 0, limit: int = 100) -> StreamingResponse:
    categories = await category.get_multi(skip=skip, limit=limit)
    return categories