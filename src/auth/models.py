from enum import Enum
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import DateTime, func, Enum as SQLAlchemyEnum, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from users.models import user_role_association, RoleModel


class Base(DeclarativeBase):
    pass


# class RoleEnum(str, Enum):
#     NOOB = "Noob"
#     MASTER = "Master"
#     BOSS = "Boss"

# user_role_association = Table(
#     "user_role_association",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
#     Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
# )


# class RoleModel(Base):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     role: Mapped[str] = mapped_column(nullable=False, unique=True)
#     users: Mapped[List["UserModel"]] = relationship(
#         "UserModel", secondary=user_role_association, back_populates="roles"
#     )


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="John")
    second_name: Mapped[str] = mapped_column(default="Dou", nullable=True)
    registration_at: Mapped[int] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # roles: Mapped[List["RoleModel"]] = relationship(
    #     "RoleModel", secondary=user_role_association, back_populates="users"
    # )  # lazy="joined"

    # role: Mapped[RoleEnum] = mapped_column(
    #     SQLAlchemyEnum(RoleEnum), default=RoleEnum.NOOB, nullable=True
    # )

    # second_name: Mapped[str]

    # hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
