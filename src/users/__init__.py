from fastapi import APIRouter
from users.router_v1 import router as user_router
from config import settings

router = APIRouter(
    # prefix=settings.api.v1.prefix,
)

router.include_router(
    user_router,
    # prefix=settings.api.v1.users,
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
