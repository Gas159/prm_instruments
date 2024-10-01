from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from tools.screws.models import ScrewModel


class ScrewBaseSchema(BaseModel):
    type: str | None = None
    length: float | None = None
    thread: str | None = None
    step_of_thread: float | None = None
    company: str | None = None
    image_path: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ScrewSchema(ScrewBaseSchema):
    # services: list[Service] = []
    id: int | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None


class ScrewCreateSchema(ScrewBaseSchema):
    # name: str
    # diameter: float
    # length_xD: float | None = None
    # deep_of_drill: float
    # plate: str | None = None
    # screw: str | None = None
    # key: str | None = None
    # company: str | None = None
    # storage: str | None = "Склад"
    # image_path: str | None = None
    # is_broken: bool | None = False
    # description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ScrewUpdateSchema(ScrewBaseSchema): ...


class ScrewDeleteSchema(BaseModel):
    id: int
