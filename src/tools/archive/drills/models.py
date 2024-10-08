from datetime import datetime


from sqlalchemy import FLOAT, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column
from project_services.base import Base
from project_services.mixins.int_id_pk import IntPkMixin


class DrillArchiveModel(Base):
    # __tablename__ = "tools"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    diameter: Mapped[float] = mapped_column(nullable=True)
    length_xD: Mapped[float] = mapped_column(nullable=True)
    deep_of_drill: Mapped[float] = mapped_column(nullable=True)
    plate: Mapped[str] = mapped_column(default="?", nullable=True)
    screw: Mapped[str] = mapped_column(default="?", nullable=True)
    key: Mapped[str] = mapped_column(default="?", nullable=True)
    company: Mapped[str] = mapped_column(default="?", nullable=True)
    is_broken: Mapped[bool] = mapped_column(default=False, nullable=True)

    image_path: Mapped[str] = mapped_column(String, nullable=True)

    # new
    storage: Mapped[str] = mapped_column(default="Cклад", nullable=True)
    description: Mapped[str] = mapped_column(default="?", nullable=True)
    create_at: Mapped[int] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # services: Mapped[List["ServiceModel"]] = relationship(
    extend_existing = True  # Позволяет обновить существующую таблицу
