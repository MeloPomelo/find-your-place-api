from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi_pagination import Params
from sqlmodel import SQLModel, select, func
from datetime import timedelta

from app.core import security
from app.core.config import settings
from app.crud import user_crud as crud
from app.crud.workspace_crud import workspace
from app.models.users_model import User
from app.models.workspace_model import Workspace
from app.schemas.response_schemas import PostResponseBase, GetResponseBase, create_response, GetResponsePaginated
from app.schemas.user_schema import UserCreate, UserRead
from app.schemas.workspace_schema import WorkspaceRead
from app.schemas.role_schema import RoleEnum
from app.schemas.token_schema import TokenRead

from app.api.endpoints import deps


router = APIRouter()


@router.post("/registartion", status_code=status.HTTP_201_CREATED)
async def registrate_user(
    # new_user: UserCreate = Depends(user_deps.user_exists),
    new_user: UserCreate,
) -> TokenRead:
    """
    Registration for new users
    """
    user = await crud.user.create_user(obj_in=new_user)
    # return create_response(data=user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("")
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
) -> GetResponseBase[UserRead]:
    """
    Gets my user profile information
    """
    return create_response(data=current_user)

@router.get("/workspaces")
async def get_user_workspaces(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user]))
) -> GetResponsePaginated[WorkspaceRead]:
    workspaces = await workspace.get_multi_paginated(
        params=params, 
        query=select(Workspace).where(Workspace.user_id==current_user.id)
    )
    # workspaces = await crud.workspace.get_user_workspaces(user_id=user_id)
    return create_response(data=workspaces)

'''
Firebase 

cred = credentials.Certificate('app/core/find-your-place-firebase-adminsdk.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('app/core/firebase_config.json')))


@router.post("/signup")
async def signup(user: UserCreate):
   email = user.email
   password = user.password
   if email is None or password is None:
       return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
   try:
       user_c = auth.create_user(
           email=email,
           password=password
       )
       return JSONResponse(content={'message': f'Successfully created user {user_c.uid}'}, status_code=200)    
   except:
       return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)
   

@router.post("/login")
async def login(user: UserCreate):
   email = user.email
   password = user.password
   try:
       user_l = pb.auth().sign_in_with_email_and_password(email, password)
       jwt = user_l['idToken']
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)
   

ping endpoint
@router.post("/ping")
async def validate(request: Request):
   headers = request.headers
   jwt = headers.get('authorization')
   print(f"jwt:{jwt}")
   user = auth.verify_id_token(jwt)
   return user["uid"]

'''
