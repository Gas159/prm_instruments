import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import mapped_column, Mapped


from config import settings
from models import Base

class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = True,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    # async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
    #     async with self.session_factory() as session:
    #         yield session

    # async def get_user_db(
    #     self, session: AsyncSession = Depends(session_getter)
    # ) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    #     yield SQLAlchemyUserDatabase(session, User)


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
