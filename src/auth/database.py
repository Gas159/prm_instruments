from typing import Annotated

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import db_helper
from sqlalchemy.ext.asyncio import AsyncSession




user = User


# session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
async def get_user_db(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    yield SQLAlchemyUserDatabase(session, User)
