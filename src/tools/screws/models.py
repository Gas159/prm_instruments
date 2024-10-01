from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_services.base import Base
from project_services.mixins.int_id_pk import IntPkMixin

# from tools.drills.models import drill_screw_association


# Винт. Тип, резьба, длинна, фирма, шаг резьбы.  Поле выдать ро резьбе и длине.


class ScrewModel(IntPkMixin, Base):
    type: Mapped[str] = mapped_column(default="?", nullable=True)
    length: Mapped[float] = mapped_column(default="?", nullable=True)
    thread: Mapped[str] = mapped_column(default="?", nullable=True)
    step_of_thread: Mapped[float] = mapped_column(default="?", nullable=True)
    company: Mapped[str] = mapped_column(default="?", nullable=True)
    image_path: Mapped[str] = mapped_column(default="?", nullable=True)
    description: Mapped[str] = mapped_column(default="?", nullable=True)
    create_at: Mapped[int] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    drills: Mapped[List["DrillModel"]] = relationship(
        "DrillModel", secondary="drill_screw_association", back_populates="screws"
    )
