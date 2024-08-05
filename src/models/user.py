from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class User(Base):
    # __tablename__ = "users"
    # id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True)
    second_name: Mapped[str]
    foo: Mapped[str]
    bar: Mapped[str]

    __table_args__ = (UniqueConstraint("foo", "bar"),)
