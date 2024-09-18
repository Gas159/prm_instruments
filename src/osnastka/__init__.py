from fastapi import APIRouter
from osnastka.router_v1 import router as utils_router
from config import settings

router = APIRouter(
    # prefix=settings.api.v1.prefix,
)

router.include_router(
    utils_router,
    # prefix=settings.api.v1,
    tags=["utils"],
    responses={404: {"description": "Not found"}},
)
