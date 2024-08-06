from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models import Base
from models.mixins.int_id_pk import IntPkMixin


class Service(IntPkMixin, Base):
    # __tablename__ = "services"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    # price: Mapped[float]
    # duration: Mapped[int]
    # user_id: Mapped[int]


# __table_args__ = (UniqueConstraint("user_id", "name"),)
