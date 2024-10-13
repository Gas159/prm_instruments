from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from starlette.responses import Response

from auth import schemas
from auth.database import get_user_db
from auth.manager import (
    fastapi_users,
    auth_backend,
    current_active_user,
    get_user_manager,
)
from auth.models import User
from auth.schemas import UserRead, UserCreate, UserUpdate

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


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


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


from fastapi import Depends, Response


@router.post("/auth/jwt/refresh")
async def refresh_jwt(response: Response, user=Depends(current_active_user)):
    return user
