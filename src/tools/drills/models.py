from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func, String, ForeignKey, Table, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_services.base import Base

from tools.screws.models import ScrewModel
from tools.plates.models import PlateModel

# Промежуточная таблица для связи ScrewModel и DrillModel
drill_screw_association = Table(
    "drill_screw_association",
    Base.metadata,
    Column("drill_id", Integer, ForeignKey("drill.id"), primary_key=True),
    Column("screw_id", Integer, ForeignKey("screw.id"), primary_key=True),
)

drill_plate_association = Table(
    "drill_plate_association",
    Base.metadata,
    Column("drill_id", Integer, ForeignKey("drill.id"), primary_key=True),
    Column("plate_id", Integer, ForeignKey("plate.id"), primary_key=True),
)
# class DrillScrewAssociation(Base):
#     drill_id: Mapped[int] = mapped_column(ForeignKey('drill.id'), primary_key=True)
#     screw_id:Mapped[int] =   mapped_column(ForeignKey('screw.id'), primary_key=True)


class DrillModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    diameter: Mapped[float] = mapped_column(nullable=True)
    length_xD: Mapped[float] = mapped_column(nullable=True)
    deep_of_drill: Mapped[float] = mapped_column(nullable=True)
    plate: Mapped[str] = mapped_column(default="?", nullable=True)
    # screw: Mapped[str] = mapped_column(default="?", nullable=True)
    key_: Mapped[str] = mapped_column(default="?", nullable=True)
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

    # Связь many-to-many с ScrewModel
    screws: Mapped[List["ScrewModel"]] = relationship(
        "ScrewModel", secondary="drill_screw_association", back_populates="drills"
    )
    plates: Mapped[List["PlateModel"]] = relationship(
        "PlateModel", secondary="drill_plate_association", back_populates="drills"
    )
