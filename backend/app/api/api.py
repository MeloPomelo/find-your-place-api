from fastapi import APIRouter
from app.api.endpoints import (
    workspace,
    comment,
    user,
    login,
)

api_router = APIRouter()
api_router.include_router(workspace.router, prefix="/workspace", tags=["workspace"])
api_router.include_router(comment.router, prefix='/comment', tags=['comment'])
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(login.router, prefix='/login', tags=['login'])
