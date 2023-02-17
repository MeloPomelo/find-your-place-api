from fastapi import APIRouter
from app.api.endpoints import (
    workspace,
)

api_router = APIRouter()
api_router.include_router(workspace.router, prefix="/workspace", tags=["workspace"])