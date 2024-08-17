from fastapi import APIRouter

from config import settings
from users.router_v1 import router as users_router
from services.router_v1 import router as services_router
from companies.router_v1 import router as companies_router

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

router.include_router(
    companies_router,
    prefix=settings.api.v1.companies,
    tags=["companies"],
    responses={404: {"description": "Not found"}},
)
