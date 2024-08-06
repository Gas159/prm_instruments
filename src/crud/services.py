from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from models.service import Service
from schemas.service import CreateService


async def get_service(
        session: AsyncSession,
        service_id: int
) -> Service:
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
    service_create: CreateService,
) -> Service:
    service = Service(**service_create.model_dump())
    session.add(service)
    await session.commit()
    # await session.refresh(service)
    return service
