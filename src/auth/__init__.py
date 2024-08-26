# from fastapi import APIRouter, Depends
# from fastapi_users import FastAPIUsers
#
# from auth.auth import auth_backend, current_active_user
# from auth.manager import get_user_manager
# from auth.models import User
#
# # from auth.models import User
# from auth.schemas import UserRead, UserCreate, UserUpdate
# from config import settings
# from users.models import UserModel
#
# fastapi_users = FastAPIUsers[UserModel, int](
#     get_user_manager,
#     [auth_backend],
# )
# router = APIRouter(
#     prefix=settings.api.v1.prefix,
# )
#
# router.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     tags=["auth"],
#     prefix=settings.api.v1.auth_jwt,
# )
#
# router.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     tags=["registration"],
#     prefix=settings.api.v1.auth,
# )
#
# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )
# @router.get("/authenticated-route")
# async def authenticated_route(user: User = Depends(current_active_user)):
#     return {"message": f"Hello {user.email}!"}
# # Пример маршрута для получения текущего пользователя
# @router.get("/users/me", response_model=UserModel)
# async def read_users_me(user: UserModel = Depends(fastapi_users.get_users_router)):
#     return user
