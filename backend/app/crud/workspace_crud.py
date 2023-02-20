from typing import Optional
from app.schemas.workspace_schema import WorkspaceCreate, WorkspaceUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.workspace_model import Workspace
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDWorkspace(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    pass


workspace = CRUDWorkspace(Workspace)