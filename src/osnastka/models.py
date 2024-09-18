from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project_services.base import Base
from project_services.mixins.int_id_pk import IntPkMixin


class ToolModel(IntPkMixin, Base):
	# __tablename__ = "tools"
	name: Mapped[str]
	diameter: Mapped[float]
	lenght: Mapped[float]
	deep_of_drill: Mapped[float]
