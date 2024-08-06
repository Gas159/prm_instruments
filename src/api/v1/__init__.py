from fastapi import APIRouter

from config import settings
from api.v1.users import router as users_router
from api.v1.services import router as services_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users,
    tags=["users"],
    responses={404: {"description": "Not found"}},
)
router.include_router(
    services_router,
    prefix=settings.api.v1.services,
    tags=["services"],
    responses={404: {"description": "Not found"}},
)
