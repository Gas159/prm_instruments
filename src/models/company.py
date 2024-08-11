from sqlalchemy import UniqueConstraint, JSON
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from models.mixins.int_id_pk import IntPkMixin
from schemas.service import Service


class CompanyModel(IntPkMixin, Base):
    __tablename__ = "companies"

    name: Mapped[str]
    description: Mapped[str]
    coordinates: Mapped[list] = mapped_column(JSON, default=[0, 0], nullable=True)

    services: Mapped[list["Service"]] = relationship(
        "ServiceModel", back_populates="company", cascade="all, delete-orphan"
    )
    # name: Mapped[str] = mapped_column(unique=True)
    # price: Mapped[float]
    # duration: Mapped[int]
    # user_id: Mapped[int]


# __table_args__ = (UniqueConstraint("user_id", "name"),)
