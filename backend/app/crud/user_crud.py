from typing import Union, Optional, List, Dict, Any
from sqlmodel import select
from fastapi_async_sqlalchemy import db

from app.db.session import AsyncSession
from app.crud.base_crud import CRUDBase
from app.models.users_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.crud import role_crud 


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(
        self, 
        *, 
        username: str, 
        db_session: Optional[AsyncSession] = None
    ) -> Optional[User]:
        db_session = db_session or db.session
        users = await db_session.execute(select(User).where(User.username == username))
        return users.scalar_one_or_none()

    async def create_user(
        self, 
        *, 
        obj_in: 
        UserCreate, 
        db_session: Optional[AsyncSession] = None
    ) -> User:
        db_session = db_session or db.session
        db_obj = User.from_orm(obj_in)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        role = await role_crud.role.get_role_by_name(
            name="user", db_session=db_session
        )

        db_obj.role_id = role.id

        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj
    

    async def create_with_role(
        self, *, obj_in: UserCreate, db_session: Optional[AsyncSession] = None
    ) -> User:
        db_session = db_session or db.session
        db_obj = User.from_orm(obj_in)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj


    async def update_is_active(
        self, 
        *, 
        db_obj: List[User], 
        obj_in: Union[int, str, Dict[str, Any]]
    ) -> Union[User, None]:
        response = None
        db_session = db_session or db.session
        for x in db_obj:
            x.is_active = obj_in.is_active
            db_session.add(x)
            await db_session.commit()
            await db_session.refresh(x)
            response.append(x)
        return response

    async def authenticate(
        self, 
        *, 
        username: str, 
        password: str
    ) -> Optional[User]:
        user = await self.get_by_username(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    

    async def add_bonuses(
        self,
        *,
        amount: int,
        user_id: int,
        db_session: Optional[AsyncSession] = None
    ) -> Optional[User]:
        db_session = db_session or db.session
        user = await self.get(id=user_id, db_session=db_session)
        user.bonus_balance += amount
        await db_session.commit()
        await db_session.refresh(user)
        return user
    

user = CRUDUser(User)