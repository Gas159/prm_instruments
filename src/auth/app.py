import logging
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from auth.manager import (
    fastapi_users,
    auth_backend,
)
from auth.models import User
from auth.schemas import UserRead, UserCreate, UserUpdate

from fastapi import Depends, Response

from database import db_helper
from users.models import UserModel

logger = logging.getLogger(__name__)

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
# session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#
# router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
current_active_user = fastapi_users.current_user(active=True)


async def current_active_user_with_roles(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: User = Depends(current_active_user),
):
    # Используем joinedload для жадной загрузки ролей
    user_id = user.id
    logger.info("Current user: %s", user_id)
    query = select(UserModel).options(joinedload(UserModel.roles)).where(UserModel.id == user_id)
    user = await session.execute(query)
    result = user.scalars().first()
    logger.info("Current user: %s", result.roles)
    return result


@router.get("/current_user")
def current_user(user: UserModel = Depends(current_active_user_with_roles)):
    logger.info("Checking role:  %s", user.roles)

    return f"Hello, {user.email}, role: {[role.role for role in user.roles]}"


# class RoleEnum(Enum):
#     NOOB = "noob"
#     MASTER = "master"
#     BOSS = "boss"


def role_checker(required_role: str):
    def role_check(user: UserModel = Depends(current_active_user_with_roles)):
        if required_role not in [role.role for role in user.roles]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return True

    # return role_check


# @router.get("/current_user_role")
# async def current_user_role(user: User = Depends(current_active_user)):
#     logger.info("Checking role: %s %s", user.role, user.email)
#     # user_role = role_checker(user.role)
#     user_str = user.role.name
#     return {"message": f"Hello {user.email}, you are {user_str}!"}


#
#
# async def get_user_role(user: User = Depends(current_active_user)) -> str:
#     return role_checker(user)


# # Функция проверки роли
# def role_checker(user: User):
#     role_str = user.role.name
#     logger.info("Checking role: %s", role_str)
#     if role_str == "NOOB":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied for NOOB")
#     return role_str

#
# async def get_user_role(user: User = Depends(current_active_user)) -> str:
#     return role_checker(user)
#
#
# @router.get("/current_user_role")
# async def current_user_role(user: User = Depends(current_active_user)):
#     logger.info("Checking role: %s %s", user.role, user.email)
#     # user_role = role_checker(user.role)
#     return {"message": f"Hello {user.email}, you are {user.role}!"}


# @router.post("/auth/jwt/refresh")
# async def refresh(
#     response: Response,
#     refresh_token: str = Cookie(None),
#     user_manager: FastAPIUsers = Depends(fastapi_users),
# ):
#     if refresh_token is None:
#         raise HTTPException(status_code=403, detail="Refresh token is missing")
#
#     # Получаем пользователя с помощью refresh токена
#     user = await user_manager.get_user_from_refresh_token(refresh_token)
#     if user is None:
#         raise HTTPException(status_code=403, detail="Invalid refresh token")
#
#     # Генерируем новые токены
#     access_token = await user_manager.get_access_token(user)
#
#     # Устанавливаем новый refresh токен в куку
#     new_refresh_token = await user_manager.create_refresh_token(user)
#     response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
#
#     return {"access_token": access_token}


# @router.post("/auth/jwt/refresh")
# async def refresh_jwt(response: Response, user=Depends(current_user)):
#     return user
