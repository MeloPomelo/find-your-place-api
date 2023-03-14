from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.crud import user_crud as crud
from app.models.users_model import User
from app.schemas.response_schemas import PostResponseBase, GetResponseBase, create_response
from app.schemas.user_schema import UserCreate, UserRead
from app.api.endpoints import deps


router = APIRouter()


@router.post("/registartion", status_code=status.HTTP_201_CREATED)
async def registrate_user(
    # new_user: UserCreate = Depends(user_deps.user_exists),
    new_user: UserCreate,
) -> PostResponseBase[UserRead]:
    """
    Registration for new users
    """
    user = await crud.user.create_user(obj_in=new_user)
    return create_response(data=user)


@router.get("")
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
) -> GetResponseBase[UserRead]:
    """
    Gets my user profile information
    """
    return create_response(data=current_user)


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
