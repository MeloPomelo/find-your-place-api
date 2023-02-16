from typing import Optional
from uuid import UUID
# from app.utils.exceptions import IdNotFoundException
from fastapi import APIRouter, Depends, Query
# from fastapi_pagination import Params
from crud import workspace_crud as crud 
# from app.api import deps
from models.workspace_model import Workspace

from schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceRead,
    WorkspaceUpdate,
)
# from app.schemas.response_schema import (
#     IDeleteResponseBase,
#     IGetResponseBase,
#     IGetResponsePaginated,
#     IPostResponseBase,
#     IPutResponseBase,
#     create_response,
# )
# from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.post("")
async def create_hero(
    workspace: WorkspaceCreate,
#     current_user: User = Depends(
#         deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
#     ),
# ) -> IPostResponseBase[IHeroRead]:
    ):
    heroe = await crud.workspace.create(obj_in=workspace)
    return "заебись создал"
