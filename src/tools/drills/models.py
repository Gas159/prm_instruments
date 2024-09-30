from datetime import datetime
from typing import List

from pygments.lexer import default
from sqlalchemy import FLOAT, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project_services.base import Base
from project_services.mixins.int_id_pk import IntPkMixin


class DrillModel(IntPkMixin, Base):
    # __tablename__ = "tools"
    name: Mapped[str]
    diameter: Mapped[float] = mapped_column(nullable=True)
    length_xD: Mapped[float] = mapped_column(nullable=True)
    deep_of_drill: Mapped[float] = mapped_column(nullable=True)
    plate: Mapped[str] = mapped_column(nullable=True)
    screw: Mapped[str] = mapped_column(nullable=True)
    key: Mapped[str] = mapped_column(nullable=True)
    company: Mapped[str] = mapped_column(nullable=True)
    is_broken: Mapped[bool] = mapped_column(default=False, nullable=True)

    # Поле для хранения пути к изображению
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    # new
    storage: Mapped[str] = mapped_column(default="Cклад", nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    create_at: Mapped[int] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # services: Mapped[List["ServiceModel"]] = relationship(
