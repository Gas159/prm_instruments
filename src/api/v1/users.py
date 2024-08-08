from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import users as users_crud
from database import db_helper
from schemas.user import UserCreate, User

router = APIRouter(
    # prefix=settings.api.v1.users,
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> User:
    user = await users_crud.get_user(session=session, user_id=user_id)
    return user


@router.get("", response_model=list[User])
async def get_all_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Sequence[User]:
    users = await users_crud.get_all_users(session=session)
    return users


@router.post("", response_model=User)
async def create_user(
    user_create: Annotated[UserCreate, Depends()],
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> User:
    user = await users_crud.create_user(session=session, user_create=user_create)
    return user
