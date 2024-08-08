from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from models.service import Service
from schemas.service import CreateService, ServiceRead
from crud import services as services_crud

router = APIRouter(
    # prefix=settings.api.v1.users,
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_all", response_model=list[ServiceRead])
async def get_all_services(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Sequence[Service]:
    services = await services_crud.get_all_services(session=session)
    return services


@router.get("/{service_id}", response_model=ServiceRead)
async def get_one_service(
    service_id: int,
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Service:
    service = await services_crud.get_service(session=session, service_id=service_id)
    return service


@router.post("/add", response_model=ServiceRead)
async def create_service(
    service_create: Annotated[CreateService, Depends()],
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Service:
    service = await services_crud.create_service(
        session=session, service_create=service_create
    )
    return service


@router.delete("/delete/{service_id}")
async def delete_service(service_id: int):

    return {"message": "Service deleted successfully"}

    # return {"error": "Service not found"}
