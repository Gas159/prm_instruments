from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import db_helper
from services import cruds as services_crud
from services.models import ServiceModel
from services.schemas import Service, ServiceBase, ServiceUpdate, CreateService


router = APIRouter()


@router.get("/service/{service_id}", response_model=Service)
async def get_one_service(
    service_id: int,
    # session: AsyncSession = Depends(db_helper.session_getter),
    # session,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ServiceModel:
    service = await services_crud.get_service(session=session, service_id=service_id)
    return service


@router.get("/services", response_model=Page[Service])
async def get_all_services(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Page[Service]:
    services = await services_crud.get_all_services(session=session)
    return services


@router.post("/service", response_model=ServiceBase)
async def create_service(
    service_create: Annotated[CreateService, Depends()],
    # service_create: CreateService,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ServiceBase:
    service = await services_crud.create_service(
        session=session, service_create=service_create
    )
    return service


@router.put("/service/{service_id}", response_model=Service)
async def update_service(
    service_id: int,
    service_update: Annotated[ServiceUpdate, Depends()],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ServiceModel:
    service = await services_crud.update_service(
        session=session, service_id=service_id, service_update=service_update
    )

    return service


@router.delete("/service/{service_id}", response_model=Service)
async def delete_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_id: int,
) -> ServiceModel:
    service = await services_crud.delete_service(session=session, service_id=service_id)
    return service
