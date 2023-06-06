from uuid import UUID
from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
)
from app.api.endpoints import deps
from app.models.users_model import User
from app.crud import visit_crud as crud
from app.crud.workspace_crud import workspace
from app.schemas.role_schema import RoleEnum
from app.schemas.visit_schema import VisitCreate, VisitUpdate, VisitRead
from app.schemas.response_schemas import (
    GetResponseBase,
    PostResponseBase, 
    PutResponseBase, 
    DeleteResponseBase,
    create_response,
)


router = APIRouter()


@router.get("/{visit_id}")
async def get_visit_by_id(
    visit_id: UUID,
) -> GetResponseBase[VisitRead]:
    """
    Gets a visit by its id
    """
    visit = await crud.visit.get(id=visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="visit not found")
    return create_response(data=visit)


@router.post("")
async def create_visit(
    visit: VisitCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin])),
) -> PostResponseBase[VisitRead]:
    """
    Add a visit on the space
    """

    new_visit = await crud.visit.create(obj_in=visit, user_id=current_user.id)
    return create_response(data=new_visit)


@router.delete("/{visit_id}")
async def delete_visit(
    visit_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> DeleteResponseBase[VisitRead]:
    """
    Delete a visit
    """
    current_visit = await crud.visit.get(id=visit_id)
    if not current_visit:
        raise HTTPException(status_code=404, detail="visit not found")
    await workspace.rating_calculation(workspace_id=current_visit.workspace_id, rating=current_visit.rating, flag=False)
    visit = await crud.visit.remove(id=visit_id)
    return create_response(visit)