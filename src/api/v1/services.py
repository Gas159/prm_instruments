from typing import Annotated, Sequence

from fastapi import APIRouter, Depends


from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper

from models import ServiceModel
from schemas.service import Service, ServiceBase, ServiceUpdate
from crud import services as services_crud

router = APIRouter(
    # prefix=settings.api.v1.users,
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{service_id}", response_model=Service)
async def get_one_service(
    service_id: int,
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ServiceModel:
    service = await services_crud.get_service(session=session, service_id=service_id)
    return service


@router.get("", response_model=list[Service])
async def get_all_services(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Sequence[ServiceModel]:
    services = await services_crud.get_all_services(session=session)
    return services


@router.post("/", response_model=Service)
async def create_service(
    service_create: Annotated[ServiceBase, Depends()],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ServiceModel:
    service = await services_crud.create_service(
        session=session, service_create=service_create
    )
    return service


@router.put("/{service_id}", response_model=Service)
async def update_item(
    service_id: int,
    service_update: Annotated[ServiceUpdate, Depends()],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ServiceModel:
    service = await services_crud.update_service(
        session=session, service_id=service_id, service_update=service_update
    )

    return service


@router.delete("/{service_id}", response_model=Service)
async def delete_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_id: int,
) -> ServiceModel:
    service = await services_crud.delete_service(session=session, service_id=service_id)
    return service
