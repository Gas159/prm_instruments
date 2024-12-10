from datetime import datetime
from typing import List
from enum import Enum
from sqlalchemy import DateTime, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_services.base import Base


class MaterialEnum(str, Enum):
    S = "s"
    M = "m"
    P = "p"


class PlateModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(default="?", nullable=True)
    sub_type: Mapped[str] = mapped_column(default="?", nullable=True)
    material: Mapped[str] = mapped_column(default="?", nullable=True)
    # material: Mapped[MaterialEnum] = mapped_column(SQLAlchemyEnum(MaterialEnum), default=MaterialEnum.M, nullable=True)
    amount: Mapped[int] = mapped_column(default=0, nullable=True)
    min_amount: Mapped[int] = mapped_column(default=0, nullable=True)
    company: Mapped[str] = mapped_column(default="?", nullable=True)

    image_path: Mapped[str] = mapped_column(default="?", nullable=True)
    description: Mapped[str] = mapped_column(default="?", nullable=True)

    create_at: Mapped[int] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    drills: Mapped[List["DrillModel"]] = relationship(
        "DrillModel",
        secondary="drill_plate_association",
        back_populates="plates",
        cascade="all, delete",
    )
