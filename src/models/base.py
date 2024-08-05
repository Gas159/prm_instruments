from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr

from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    # __tablename__: str = camel_case_to_snake_case(__name__)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    id: Mapped[int] = mapped_column(primary_key=True)
