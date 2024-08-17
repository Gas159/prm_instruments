from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from api_v1 import get_user_manager
from api_v1 import User
from api_v1 import UserRead, UserCreate
from config import settings

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["auth"],
    prefix=settings.api.v1.auth_jwt,
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["registration"],
    prefix=settings.api.v1.auth,
)