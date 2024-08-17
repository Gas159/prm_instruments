from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from project_services.base import Base
from project_services.mixins.int_id_pk import IntPkMixin


class User(IntPkMixin, Base):
    username: Mapped[str]  # = mapped_column(unique=True)
    second_name: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    # role_id: Mapped[int] = mapped_column(ForeignKey("role.c.id"), nullable=False)

    # registration_at: Mapped[int] = mapped_column(
    #     TIMESTAMP, nullable=False, default=datetime.datetime.now(datetime.UTC)
    # )
    registration_at: Mapped[int] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # id: Mapped[int] = mapped_column(primary_key=True)
    # username: Mapped[str] = mapped_column(unique=True)
    # foo: Mapped[str]
    # bar: Mapped[str]

    # __table_args__ = (UniqueConstraint("foo", "bar"),)
