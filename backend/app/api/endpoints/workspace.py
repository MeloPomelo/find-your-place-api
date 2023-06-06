from io import BytesIO
from typing import List, Union, Optional
from uuid import UUID
from sqlmodel import select, and_
from fastapi_pagination import Params
from fastapi_async_sqlalchemy import db
from fastapi import (
    APIRouter, 
    Depends, 
    Query, 
    HTTPException, 
    UploadFile, 
    File,
    Response
)

from app.api.endpoints import deps
from app.utils.resize_image import modify_image
from app.utils.minio_client import MinioClient
from app.models import User, Workspace
from app.crud import (
    workspace_crud,
    image_media_crud,
    parameter_crud,
    status_crud,
    comment_crud
)
from app.schemas.role_schema import RoleEnum
from app.schemas.media_schema import MediaCreate
from app.schemas.image_media_schema import ImageMediaCreate
from app.schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceRead,
    WorkspaceUpdate,
    WorkspaceDelete,
)
from app.schemas.response_schemas import (
    GetResponseBase,
    GetResponsePaginated,
    PostResponseBase, 
    PutResponseBase, 
    DeleteResponseBase,
    create_response,
)


router = APIRouter()


@router.get("")
async def get_by_parameters(
    search: Union[str, None] = None,
    rooms: Union[List[str], None] = Query(default=None),
    additional: Union[List[str], None] = Query(default=None),
    features: Union[List[str], None] = Query(default=None),
    params: Params = Depends(),
) -> GetResponsePaginated[WorkspaceRead]:
    query_items = {}
    query_items['rooms'] = rooms
    query_items['additional'] = additional
    query_items['features'] = features
    a = []
    for key in query_items.keys():
        if query_items[key]:
            a += [Workspace.parameters.property.mapper.c.code_name == i for i in query_items[key]]
    
    query = select(Workspace).join(Workspace.status).where(Workspace.status.property.mapper.c.code_name == "approved")
    if a:
        query = query.join(Workspace.parameters).where(and_(*a))
    if search:
        query = query.filter(Workspace.title.startswith(search))
    workspaces = await workspace_crud.workspace.get_multi_paginated(params=params, query=query)
    return create_response(data=workspaces)


@router.get("/{workspace_id}")
async def get_workspace_by_id(
    workspace_id: UUID,
) -> GetResponseBase[WorkspaceRead]:
    """
    Gets a workspace by its id
    """
    workspace = await workspace_crud.workspace.get(id=workspace_id)
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
    new_workspace = await workspace_crud.workspace.create(obj_in=workspace, user_id=current_user.id)

    status = await status_crud.status.get_status_by_code_name(code_name="handling", db_session=db.session)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    new_workspace = await workspace_crud.workspace.set_status(workspace=new_workspace, status=status)

    for image_id in workspace.images_id:
        image = await image_media_crud.image_media.get(id=image_id)
        if not image: 
            raise HTTPException(status_code=404, detail="Image not found")
        new_workspace = await workspace_crud.workspace.add_image_to_workspace(workspace=new_workspace, image_id=image_id)

    for paramter_code_name in workspace.parameters:
        paramter = await parameter_crud.parameter.get_parameter_by_code_name(code_name=paramter_code_name, db_session=db.session)
        if not paramter:
            raise HTTPException(status_code=404, detail="Parameter not found")
        new_workspace = await workspace_crud.workspace.add_parameter_to_workspace(workspace=new_workspace, parameter=paramter)

    return create_response(data=new_workspace) 


@router.put("/{workspace_id}")
async def update_workspace(
    workspace_id: UUID,
    workspace: WorkspaceUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> PutResponseBase[WorkspaceRead]:
    """
    Upadate a workspace
    """
    current_workspace = await workspace_crud.workspace.get(id=workspace_id)
    if not current_workspace:
        raise HTTPException(status_code=404, detail="Worksapce not found")
    
    merge_images = workspace.images_id[:]
    merge_parameters = workspace.parameters[:]

    for image in current_workspace.images:
        if not image.id in workspace.images_id:
            await workspace_crud.workspace.remove_image_from_workspace(workspace=current_workspace, image_id= image.id)
        else:
            merge_images.remove(image.id)

    for parameter in current_workspace.parameters:
        if not parameter.code_name in workspace.parameters:
            parameter = await parameter_crud.parameter.get_parameter_by_code_name(code_name=parameter.code_name, db_session=db.session)
            await workspace_crud.workspace.remove_parameter_from_workspace(workspace=current_workspace, parameter=parameter)
        else:
            merge_parameters.remove(parameter.code_name)

    for image_id in merge_images:
        image = await image_media_crud.image_media.get(id=image_id)
        if not image: 
            raise HTTPException(status_code=404, detail="Image not found")
        current_workspace = await workspace_crud.workspace.add_image_to_workspace(workspace=current_workspace, image_id=image_id)

    for paramter_code_name in workspace.parameters:
        paramter = await parameter_crud.parameter.get_parameter_by_code_name(code_name=paramter_code_name, db_session=db.session)
        if not paramter:
            raise HTTPException(status_code=404, detail="Parameter not found")
        current_workspace = await workspace_crud.workspace.add_parameter_to_workspace(workspace=current_workspace, parameter=paramter)

    workspace_updated = await workspace_crud.workspace.update(obj_new=workspace, obj_current=current_workspace)
    return create_response(data=workspace_updated)


@router.delete("/{workspace_id}")
async def delete_workspace(
    workspace_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> DeleteResponseBase[WorkspaceDelete]:
    """
    Delete a workspace
    """
    current_workspace = await workspace_crud.workspace.get(id=workspace_id)
    if not current_workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    for comment in current_workspace.comments:
        await comment_crud.comment.remove(id=comment.id)

    for image in current_workspace.images:
        await image_media_crud.image_media.remove(id=image.id)

    workspace = await workspace_crud.workspace.remove(id=workspace_id)
    return create_response(workspace)


@router.post("/upload_image")
async def upload_image(
    image_file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
    minio_client: MinioClient = Depends(deps.minio_auth),
) -> PostResponseBase[ImageMediaCreate]:
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
        return Response("Internal server error", status_code=500)
    
