import json

import aioredis


from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page

from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from companies.models import CompanyModel
from companies.schemas import SCompanyCreate, SCompanyUpdate, SCompany


async def get_company(
    session: AsyncSession,
    company_id: int,
) -> SCompany:
    stmt = (
        select(CompanyModel)
        .options(selectinload(CompanyModel.services))
        .where(CompanyModel.id == company_id)
    )
    company = await session.scalar(stmt)
    # company = company_tuple.first()
    if company is None:
        raise HTTPException(status_code=404, detail="company not found")
    return jsonable_encoder(company)


async def get_all_companies(
    session: AsyncSession,
) -> Page[SCompany]:  # Sequence[SCompany]:
    redis = aioredis.from_url("redis://localhost")
    redis_key = "all_companies"
    cached_data = await redis.get(redis_key)

    if cached_data:
        # Если данные есть в кэше, десериализуйте их и верните
        companies = [SCompany(**company) for company in json.loads(cached_data)]
        return Page.create(companies, params=None)  # Подставьте правильные параметры

    # Если данных в кэше нет, выполните запрос к базе данных
    stmt = (
        select(CompanyModel)
        .options(selectinload(CompanyModel.services))
        .order_by(CompanyModel.id)
    )
    result = await paginate(query=stmt, conn=session)

    # Сериализация и сохранение результата в Redis
    serialized_result = json.dumps([company.dict() for company in result.items])
    await redis.set(redis_key, serialized_result, ex=3600)  # Данные будут храниться в кэше 1 час

    return result


async def create_company(
    session: AsyncSession,
    company_create: SCompanyCreate,
) -> SCompanyCreate:
    company = CompanyModel(**company_create.model_dump())
    session.add(company)
    await session.commit()
    # await session.refresh(company)
    return jsonable_encoder(company)
    # return company


async def update_company(
    session: AsyncSession,
    company_update: SCompanyUpdate,
    company_id: int,
) -> SCompany:
    stmt = select(CompanyModel).where(CompanyModel.id == company_id)
    company = await session.scalar(stmt)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company_update.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        setattr(company, key, value)
    await session.commit()
    await session.refresh(company)
    return jsonable_encoder(company)


async def delete_company(
    session: AsyncSession,
    company_id: int,
) -> SCompany:
    stmt = select(CompanyModel).where(CompanyModel.id == company_id)
    result = await session.scalars(stmt)
    company = result.first()
    if company is None:
        raise HTTPException(status_code=404, detail="company not found")
    await session.delete(company)
    await session.commit()
    return SCompany(**company.model_dump())  # type: ignore[no-any-return]  # noqa company
