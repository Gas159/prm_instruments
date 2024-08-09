from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Service
from schemas.service import CreateService, ServiceBase


async def get_service(session: AsyncSession, service_id: int) -> Service:
    stmt = select(Service).where(Service.id == service_id)
    res = await session.scalars(stmt)
    return res.first()


async def get_all_services(
    session: AsyncSession,
) -> Sequence[Service]:
    stmt = select(Service).order_by(Service.id)
    # services = await session.scalars(select(Service).order_by(Service.id))
    services = await session.scalars(stmt)
    return services.all()


async def create_service(
    session: AsyncSession,
    service_create: CreateService,  # schema: CreateService
) -> Service:
    service = Service(**service_create.model_dump())
    session.add(service)
    await session.commit()
    # await session.refresh(service)
    return service


async def delete_service(
    session: AsyncSession,
    service_id: int,
) -> Service:
    stmt = select(Service).where(Service.id == service_id)
    result = await session.scalars(stmt)
    service = result.first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    await session.delete(service)
    await session.commit()
    return service
