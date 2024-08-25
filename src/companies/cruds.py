import json

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from companies.models import CompanyModel
from companies.schemas import SCompanyCreate, SCompanyUpdate, SCompany
from y_project_services.redis_tools import redis


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


async def get_company(
    session: AsyncSession,
    company_id: int,
) -> SCompany:
    redis_key = "company_" + str(company_id)
    cached_data = await redis.get(redis_key)

    if cached_data:
        print(f"Loaded data from Redis: ")
        company_data = json.loads(cached_data.decode("utf-8"))
        return SCompany(**company_data)

    stmt = (
        select(CompanyModel)
        .options(selectinload(CompanyModel.services))
        .where(CompanyModel.id == company_id)
    )
    company = await session.scalar(stmt)
    # company = company_tuple.first()
    if company is None:
        raise HTTPException(status_code=404, detail="company not found")

    company_dict = model_to_dict(company)
    # Сериализация и сохранение результата в Redis
    serialized_data = json.dumps(company_dict)
    await redis.set(redis_key, serialized_data, ex=10)
    print(f"Saved data to Redis: ")

    return SCompany(**company_dict)
    # return jsonable_encoder(company)


async def get_all_companies(
    session: AsyncSession,
    params: Params,
) -> Page[SCompany]:  # Sequence[SCompany]:
    redis_key: str = f'all_companies:{str(params.size)}:{str(params.page)}'
    cached_data = await redis.get(redis_key)

    # Если данные есть в Redis, то возвращаем их
    if cached_data:
        print(f"Loaded data from Redis: ")
        cached_data = json.loads(cached_data)
        companies = [SCompany(**company) for company in cached_data['companies']]

        return Page.create(companies, total=int(cached_data['total']), params=params)

    stmt = (
        select(CompanyModel)
        .options(selectinload(CompanyModel.services))
        .order_by(CompanyModel.id)
    )
    result = await paginate(query=stmt, conn=session)
    # print(result, type(result), result.items, type(result.items), sep="\n")

    # Сериализация и сохранение результата в Redis
    serialized_result = json.dumps(
        {'companies': [company.model_dump() for company in result.items], 'total': result.total}
    )
    await redis.set(redis_key, serialized_result, ex=10)
    print(f"Saved data to Redis: ")
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
