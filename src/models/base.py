from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from config import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        # naming_convention={
        #     "ix": "ix_%(column_0_label)s",
        #     "uq": "uq_%(table_name)s_%(column_0_name)s",
        #     "ck": "ck_%(table_name)s_%(constraint_name)s",
        #     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        #     "pk": "pk_%(table_name)s",
        # }
        naming_convention=settings.db.naming_convention,
    )

    # __tablename__: str = camel_case_to_snake_case(__name__)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    # id: Mapped[int] = mapped_column(primary_key=True) #вынесено в IntPkMixin
