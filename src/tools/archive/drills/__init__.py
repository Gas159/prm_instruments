from fastapi import APIRouter
from tools.archive.drills.api import router as drill_router
from config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    drill_router,
    # prefix="/drills_archive",
    tags=["Drills_archive"],
    responses={404: {"description": "Not found"}},
)
