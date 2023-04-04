from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.core import security
from app.core.config import settings
from app.crud import user_crud as crud
from app.schemas.response_schemas import PostResponseBase, create_response
from app.schemas.token_schema import TokenRead, Token, RefreshToken
from app.schemas.user_schema import LoginSchema


router = APIRouter()


@router.post("")
async def login_access_token(
    form_data: LoginSchema
    # form_data: OAuth2PasswordRequestForm = Depends(),
    # redis_client: Redis = Depends(get_redis_client),
) -> TokenRead:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    '''
    For furure Redis integration
    
        valid_access_tokens = await get_valid_tokens(
        redis_client, user.id, TokenType.ACCESS
    )
    if valid_access_tokens:
        await add_token_to_redis(
            redis_client,
            user,
            access_token,
            TokenType.ACCESS,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    
    '''

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/access-token")
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    # redis_client: Redis = Depends(get_redis_client),
) -> TokenRead:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    '''
    For furure Redis integration
    
        valid_access_tokens = await get_valid_tokens(
        redis_client, user.id, TokenType.ACCESS
    )
    if valid_access_tokens:
        await add_token_to_redis(
            redis_client,
            user,
            access_token,
            TokenType.ACCESS,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    
    '''

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token")
async def login_refresh_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> PostResponseBase[Token]:
    """
    Login for all users
    """
    user = await crud.user.authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email or Password incorrect")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user=user,
    )
    '''
    For furure Redis integration

    valid_access_tokens = await get_valid_tokens(
        redis_client, user.id, TokenType.ACCESS
    )
    if valid_access_tokens:
        await add_token_to_redis(
            redis_client,
            user,
            access_token,
            TokenType.ACCESS,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    valid_refresh_tokens = await get_valid_tokens(
        redis_client, user.id, TokenType.REFRESH
    )
    if valid_refresh_tokens:
        await add_token_to_redis(
            redis_client,
            user,
            refresh_token,
            TokenType.REFRESH,
            settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
    '''
    return create_response(data=data, message="Login correctly")


