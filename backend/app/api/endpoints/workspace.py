from io import BytesIO
from typing import Optional, List
from uuid import UUID
from fastapi_pagination import Params
from fastapi import (
    APIRouter, 
    Depends, 
    Query, 
    HTTPException, 
    Body, 
    UploadFile, 
    File,
    Response
)
from app.api.endpoints import deps
from app.utils.resize_image import modify_image
from app.utils.minio_client import MinioClient
from app.models.users_model import User
from app.models.workspace_model import Workspace
from app.models.image_media_model import ImageMedia
from app.schemas.role_schema import RoleEnum
from app.crud import workspace_crud as crud 
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
from app.schemas.media_schema import MediaCreate


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


@router.post("/image")
async def upload_my_image(
    workspace_id: UUID,
    title: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    image_file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
    minio_client: MinioClient = Depends(deps.minio_auth),
) -> PostResponseBase[ImageMedia]:
    """
    Uploads a workspace image
    """
    try:
        image_modified = modify_image(BytesIO(image_file.file.read()))
        data_file = minio_client.put_object(
            file_name=image_file.filename,
            file_data=BytesIO(image_modified.file_data),
            content_type=image_file.content_type,
        )
        media = MediaCreate(
            title=title, description=description, path=data_file.file_name
        )

        image_media = await crud.workspace.update_photo(
            workspace_id=workspace_id,
            image=media,
            heigth=image_modified.height,
            width=image_modified.width,
            file_format=image_modified.file_format,
        )

        return create_response(data=image_media)
    except Exception as e:
        print(e)
        return Response("Internal server error", status_code=500)