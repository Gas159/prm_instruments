from typing import List

from pygments.lexer import default
from sqlalchemy import FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project_services.base import Base
from project_services.mixins.int_id_pk import IntPkMixin


class ToolModel(IntPkMixin, Base):
    # __tablename__ = "tools"
    name: Mapped[str]
    diameter: Mapped[float] = mapped_column(default=0.0, nullable=True)
    length: Mapped[float] = mapped_column(default=0.0, nullable=True)
    deep_of_drill: Mapped[float] = mapped_column(default=0.0, nullable=True)
    plate: Mapped[str] = mapped_column(nullable=True)
    screws: Mapped[str] = mapped_column(nullable=True)
    key: Mapped[str] = mapped_column(nullable=True)
    company: Mapped[str] = mapped_column(nullable=True)
    is_broken: Mapped[bool] = mapped_column(default=False, nullable=True)
    # services: Mapped[List["ServiceModel"]] = relationship(
