# from typing import Sequence
# from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.models import ServiceModel
from services.schemas import ServiceBase, ServiceUpdate, Service, CreateService


async def get_service(
    session: AsyncSession,
    service_id: int,
) -> ServiceModel:
    stmt = select(ServiceModel).where(ServiceModel.id == service_id)
    service = await session.scalar(stmt)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


async def get_all_services(
    session: AsyncSession,
) -> Page[Service]:
    stmt = select(ServiceModel).options(joinedload(ServiceModel.company)).order_by(ServiceModel.id)
    return await paginate(query=stmt, conn=session)


async def create_service(
    session: AsyncSession,
    service_create: CreateService,  # schema: CreateService
) -> ServiceBase:
    service = ServiceModel(**service_create.model_dump())
    session.add(service)
    await session.commit()
    # await session.refresh(service)
    return jsonable_encoder(service)


async def update_service(
    session: AsyncSession,
    service_update: ServiceUpdate,
    service_id: int,
) -> ServiceModel:
    stmt = select(ServiceModel).where(ServiceModel.id == service_id)
    service = await session.scalar(stmt)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    for key, value in service_update.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        setattr(service, key, value)
    await session.commit()
    await session.refresh(service)
    return service


async def delete_service(
    session: AsyncSession,
    service_id: int,
) -> ServiceModel:
    stmt = select(ServiceModel).where(ServiceModel.id == service_id)
    result = await session.scalars(stmt)
    service = result.first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    await session.delete(service)
    await session.commit()
    return service
