from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreate


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User:
    stmt = select(User).where(User.id == user_id)
    res = await session.scalars(stmt)
    return res.first()


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    res = await session.scalars(stmt)
    return res.all()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user
