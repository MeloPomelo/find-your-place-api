from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from uuid import UUID

from app.crud import dictionary_crud as crud
from app.models.dictionary_model import Dictionary
from app.schemas.response_schemas import PostResponseBase, GetResponseBase, DeleteResponseBase, create_response
from app.schemas.dictionary_schema import DictionaryCreate, DictionaryRead
from app.api.endpoints import deps
from app.schemas.role_schema import RoleEnum
from app.models.users_model import User


router = APIRouter()


@router.post("/create_dictionary")
async def create_dictionary(
    dictionary: DictionaryCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> PostResponseBase[DictionaryRead]:
    print("\n",dictionary, '\n')
    dictionary = await crud.dictionary.create(obj_in=dictionary)

    return create_response(data=dictionary)


@router.get("/{dictionary_id}")
async def get_dictionary_list(
    dictionary_id: UUID,
) -> GetResponseBase[DictionaryRead]:
    dictionary = await crud.dictionary.get(id=dictionary_id)
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")
    return create_response(data=dictionary)


@router.delete("/delete_dictionary")
async def delete_dictionary(
    dictionary_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin]))
) -> DeleteResponseBase[DictionaryRead]:

    cur_dictionary = await crud.dictionary.get(id=dictionary_id)

    if not cur_dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")
    dictionary = await crud.dictionary.remove(id=dictionary_id)
    return create_response(dictionary)