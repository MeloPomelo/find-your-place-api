from typing import AsyncGenerator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.models.users_model import User
from pydantic import ValidationError
from app.crud import user_crud as crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.token_schema import TokenType
from app.utils.minio_client import MinioClient


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)


def get_current_user(required_roles: List[str] = None) -> User:
    async def current_user(
        token: str = Depends(reusable_oauth2),
    ) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user_id = payload["sub"]
        user: User = await crud.user.get(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True

            if not is_valid_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"""Role "{required_roles}" is required for this action""",
                )

        return user

    return current_user


def minio_auth() -> MinioClient:
    minio_client = MinioClient(
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket_name=settings.MINIO_BUCKET,
        minio_url=settings.MINIO_URL,
    )
    return minio_client