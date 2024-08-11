from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from models.mixins.int_id_pk import IntPkMixin


class ServiceModel(IntPkMixin, Base):
    # __tablename__ = "services"

    name: Mapped[str]
    description: Mapped[str]
    comment: Mapped[str] = mapped_column(nullable=True)
    rate: Mapped[int] = mapped_column(default=0, nullable=True)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=True)

    company: Mapped["CompanyModel"] = relationship(
        "CompanyModel", back_populates="services"
    )

    # name: Mapped[str] = mapped_column(unique=True)
    # price: Mapped[float]
    # duration: Mapped[int]
    # user_id: Mapped[int]


# __table_args__ = (UniqueConstraint("user_id", "name"),)
