from fastapi import APIRouter
from services.router_v1 import router as service_router
from config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    service_router,
    # prefix=settings.api.v1.services,
    tags=["Services"],
    responses={404: {"description": "Not found"}},
)
