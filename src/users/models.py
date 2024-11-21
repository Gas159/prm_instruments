from typing import List

from sqlalchemy import String, Boolean, DateTime, func, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from project_services.base import Base

# class RoleEnum(str, Enum):
#     NOOB = "Noob"
#     MASTER = "Master"
#     BOSS = "Boss"

user_role_association = Table(
    "user_role_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)


class RoleModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False, unique=True)
    users: Mapped[List["UserModel"]] = relationship(
        "UserModel", secondary=user_role_association, back_populates="roles"
    )


class UserModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(default="John1", nullable=False)
    last_name: Mapped[str] = mapped_column(default="Dou", nullable=True)
    position: Mapped[str | None] = mapped_column(default="worker", nullable=True)
    phone_number: Mapped[str | None] = mapped_column(
        String(length=15), default=None, unique=True, index=True, nullable=True
    )

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    registration_at: Mapped[int] = mapped_column(DateTime(timezone=True), server_default=func.now())

    roles: Mapped[List["RoleModel"]] = relationship(
        "RoleModel", secondary=user_role_association, back_populates="users"
    )  # lazy="joined"

    hashed_password: Mapped[bytes] = mapped_column(String(length=1024), default='123', nullable=False)


# role: Mapped[RoleEnum] = mapped_column(SQLAlchemyEnum(RoleEnum), default=RoleEnum.NOOB, nullable=True)
