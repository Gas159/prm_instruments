# from fastapi import APIRouter
# from tools.drill import router as drill_router
# from config import settings
#
# router = APIRouter(
#     prefix=settings.api.prefix,
# )
#
# router.include_router(
#     drill_router,
#     # prefix="/drills",
#     tags=["Drills"],
#     responses={404: {"description": "Not found"}},
# )
