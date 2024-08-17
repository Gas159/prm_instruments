from fastapi import APIRouter
from companies.router_v1 import router as company_router
from config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    company_router,
    prefix=settings.api.v1.companies,
    tags=["Companies"],
    responses={404: {"description": "Not found"}},
)
