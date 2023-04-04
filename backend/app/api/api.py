from fastapi import APIRouter
from app.api.endpoints import (
    workspace,
    user,
    login,
    dictionary
)

api_router = APIRouter()
api_router.include_router(workspace.router, prefix="/workspace", tags=["workspace"])
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(login.router, prefix='/login', tags=['login'])
api_router.include_router(dictionary.router, prefix='/dictionary', tags=['dictionary'])