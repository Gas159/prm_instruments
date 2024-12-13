from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_services.base import Base


# Винт. Тип, резьба, длинна, фирма, шаг резьбы.  Поле выдать ро резьбе и длине.


class ScrewModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(default="?", nullable=True)
    length: Mapped[float] = mapped_column(default=0, nullable=True)
    thread: Mapped[str] = mapped_column(default="?", nullable=True)
    step_of_thread: Mapped[float] = mapped_column(default=0, nullable=True)
    company: Mapped[str] = mapped_column(default="?", nullable=True)
    image_path: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(default="?", nullable=True)

    create_at: Mapped[int] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    drills: Mapped[List["DrillModel"]] = relationship(
        "DrillModel",
        secondary="drill_screw_association",
        back_populates="screws",
    )
