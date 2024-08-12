import datetime
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import  String, Boolean, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from database import db_helper
from models import Base
from models.mixins.int_id_pk import IntPkMixin

# DATABASE_URL = "sqlite+aiosqlite:///./test.db"


# class Base(DeclarativeBase):
#     pass


# class User(SQLAlchemyBaseUserTableUUID, Base):
#     pass
class User(SQLAlchemyBaseUserTable[int], Base):
    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    second_name: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    # role_id: Mapped[int] = mapped_column(ForeignKey("role.c.id"), nullable=False)

    registration_at: Mapped[int] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.datetime.now(datetime.UTC)
    )

    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

user = User()
# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# @router.get("/{company_id}", response_model=SCompany)
# async def get_one_company(
#     company_id: int,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ) -> SCompany:

# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(session, User)
