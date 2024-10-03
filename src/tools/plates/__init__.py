from fastapi import APIRouter
from tools.plates.api import router as screw_router
from config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    screw_router,
    # prefix="/screw",
    tags=["Plates"],
    responses={404: {"description": "Not found"}},
)
