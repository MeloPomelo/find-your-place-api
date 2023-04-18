from io import BytesIO
from typing import Optional, List
from uuid import UUID
from fastapi_pagination import Params
from fastapi_async_sqlalchemy import db
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
from app.models.comment_model import Comment
from app.crud import workspace_crud as crud 
from app.crud import image_media_crud
from app.crud import parameter_crud
from app.schemas.role_schema import RoleEnum
from app.schemas.media_schema import MediaCreate
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

from app.schemas.category_schema import CategoryRead
from app.crud.category_crud import category

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


@router.post("")
async def create_workspace(
    workspace: WorkspaceCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> PostResponseBase[WorkspaceRead]:
    """
    Create a new workspace
    """
    new_workspace = await crud.workspace.create(obj_in=workspace)

    for image_id in workspace.images_id:
        image = await image_media_crud.image_media.get(id=image_id)
        if not image: 
            raise HTTPException(status_code=404, detail="Image not found")
        new_workspace = await crud.workspace.add_image_to_workspace(workspace=new_workspace, image_id=image_id)

    for paramter_title in workspace.parameters:
        paramter = await parameter_crud.parameter.get_parameter_by_name(title=paramter_title, db_session=db.session)
        if not paramter:
            raise HTTPException(status_code=404, detail="Parameter not found")
        new_workspace = await crud.workspace.add_parameters_to_workspace(workspace=new_workspace, parameter=paramter)

    return create_response(data=new_workspace) 


@router.put("/{workspace_id}")
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


@router.delete("/{workspace_id}")
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


@router.post("/upload_image")
async def upload_image(
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
            path=data_file.file_name
        )

        image_media = await image_media_crud.image_media.upload_image(
            image=media,
        )

        return create_response(data=image_media)
    except Exception as e:
        print(e)
        return Response("Internal server error", status_code=500)
    
