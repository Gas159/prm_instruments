from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_helper
from schemas.company import SCompany, SCompanyCreate, SCompanyUpdate
from crud import companies as companies_crud
from fastapi_pagination import Page


router = APIRouter(
    # prefix=settings.api.v1.users,
    # tags=["companies"],
    # responses={404: {"description": "Not found"}},
)


@router.get("/{company_id}", response_model=SCompany)
async def get_one_company(
    company_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> SCompany:
    company = await companies_crud.get_company(session=session, company_id=company_id)
    return company


@router.get("", response_model=Page[SCompany])
async def get_all_services(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Page[SCompany]:
    companies = await companies_crud.get_all_companies(session=session)
    return companies
    # stmt = (
    #     select(CompanyModel).options(selectinload(CompanyModel.services))
    #     .order_by(CompanyModel.id)
    # )
    # result = await session.execute(stmt)
    # companies = result.scalars().all()
    # Возвращаем отформатированные данные с пагинацией
    # return await paginate(session, stmt)


@router.post("/", response_model=SCompanyCreate)
async def create_service(
    company_create: Annotated[SCompanyCreate, Depends()],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> SCompanyCreate:
    service = await companies_crud.create_company(
        session=session, company_create=company_create
    )
    return service


@router.put("/{companies_id}", response_model=SCompany)
async def update_company(
    company_id: int,
    company_update: Annotated[SCompanyUpdate, Depends()],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> SCompany:
    company = await companies_crud.update_company(
        session=session, company_id=company_id, company_update=company_update
    )

    return company


@router.delete("/{companies_id}", response_model=SCompany)
async def delete_company(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    company_id: int,
) -> SCompany:
    service = await companies_crud.delete_company(
        session=session, company_id=company_id
    )
    return service
