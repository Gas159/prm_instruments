from abc import ABC, abstractmethod
from select import select
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from services.schemas import ServiceBase


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, data, session):
        pass

    # @abstractmethod
    # async def get_one(self): ...
    @abstractmethod
    async def get_all(self): ...


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(
        self,
        data: dict,
        session: AsyncSession,
    ) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await session.execute(stmt)
        await session.commit()
        # res.scalars().first()
        return res.scalar_one()

    async def get_all(self, **filter_by) -> list:
        async with db_helper.session_getter as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()


# @router.post("/service", response_model=ServiceBase)
# async def create_service(
#     service_create: Annotated[CreateService, Depends()],
#     # service_create: CreateService,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ) -> ServiceBase:
#     service = await services_crud.create_service(
#         session=session, service_create=service_create
#     )
#     return service

# async def create_service(
#     session: AsyncSession,
#     service_create: CreateService,  # schema: CreateService
# ) -> ServiceBase:
#     service = ServiceModel(**service_create.model_dump())
#     session.add(service)
#     await session.commit()
#     # await session.refresh(service)
#     return jsonable_encoder(service)
