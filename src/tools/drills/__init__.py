from fastapi import APIRouter
from tools.drills.api import router as drill_router
from config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    drill_router,
    prefix="/drill",
    tags=["Drills"],
    responses={404: {"description": "Not found"}},
)
