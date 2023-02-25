from fastapi import APIRouter
from app.api.endpoints import (
    workspace,
    user,
)

api_router = APIRouter()
api_router.include_router(workspace.router, prefix="/workspace", tags=["workspace"])
api_router.include_router(user.router, prefix='/user', tags=['user'])