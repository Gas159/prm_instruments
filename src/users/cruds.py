from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import UserModel
from users.schemas import UserCreateSchema


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> UserModel:
    stmt = select(UserModel).where(UserModel.id == user_id)
    service_tuple = await session.scalars(stmt)
    user = service_tuple.first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # res = await session.scalars(stmt)
    # return res.first()
    return user


async def get_all_users(
    session: AsyncSession,
) -> Sequence[UserModel]:
    stmt = select(UserModel).order_by(UserModel.id)
    res = await session.scalars(stmt)
    return res.all()


async def create_user(
    session: AsyncSession,
    user_create: UserCreateSchema,
) -> UserModel:
    user = UserModel(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user
