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
from app.models.users_model import User
from app.crud import comment_crud as crud
from app.crud.workspace_crud import workspace
from app.schemas.role_schema import RoleEnum
from app.schemas.response_schemas import (
    GetResponseBase,
    GetResponsePaginated,
    PostResponseBase, 
    PutResponseBase, 
    DeleteResponseBase,
    create_response,
)
from app.schemas.comment_schema import (
    CommentCreate,
    CommentUpdate,
    CommentRead
)


router = APIRouter()


@router.get("/{comment_id}")
async def get_comment_by_id(
    comment_id: UUID,
) -> GetResponseBase[CommentRead]:
    """
    Gets a comment by its id
    """
    comment = await crud.comment.get(id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return create_response(data=comment)


@router.post("")
async def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin])),
) -> PostResponseBase[CommentRead]:
    """
    Add a comment on the space
    """
    new_comment = await crud.comment.create(obj_in=comment)
    await workspace.rating_calculation(workspace_id=comment.workspace_id, rating=comment.rating)
    return create_response(data=new_comment)


@router.put("/{comment_id}")
async def update_comment(
    comment_id: UUID,
    comment: CommentUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> PutResponseBase[CommentRead]:
    """
    Update a comment
    """
    current_comment = await crud.comment.get(id=comment_id)
    if not current_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment_updated = await crud.comment.update(obj_new=comment, obj_current=current_comment)
    return create_response(data=comment_updated)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> DeleteResponseBase[CommentRead]:
    """
    Delete a comment
    """
    current_comment = await crud.comment.get(id=comment_id)
    if not current_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await workspace.rating_calculation(workspace_id=current_comment.workspace_id, rating=current_comment.rating, flag=False)
    comment = await crud.comment.remove(id=comment_id)
    return create_response(comment)