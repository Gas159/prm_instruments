from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import ServiceModel
from schemas.service import ServiceBase, ServiceUpdate


async def get_service(
    session: AsyncSession,
    service_id: int,
) -> ServiceModel:
    stmt = select(ServiceModel).where(ServiceModel.id == service_id)
    service = await session.scalar(stmt)
    # service = service_tuple.first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


async def get_all_services(
    session: AsyncSession,
) -> Sequence[ServiceModel]:
    stmt = select(ServiceModel).order_by(ServiceModel.id)
    # ServiceModels = await session.scalars(select(ServiceModel).order_by(ServiceModel.id))
    services = await session.scalars(stmt)
    return services.all()


async def create_service(
    session: AsyncSession,
    service_create: ServiceBase,  # schema: CreateService
) -> ServiceModel:
    service = ServiceModel(**service_create.model_dump())
    session.add(service)
    await session.commit()
    # await session.refresh(service)
    return service


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
