from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DrillArchiveBaseSchema(BaseModel):
    name: str = "test"
    diameter: float | None = 0
    length_xD: float | None = 0
    deep_of_drill: float | None = 0
    plate: str | None = None
    screw: str | None = None
    key: str | None = None
    company: str | None = None
    is_broken: bool | None = False
    # image_path: List[str] | None = None
    storage: str | None = "Склад"
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DrillArchiveSchema(DrillArchiveBaseSchema):
    # services: list[Service] = []
    id: int
    image_path: Optional[str] = None

    create_at: datetime
    update_at: datetime


class DrillCreateSchema(DrillArchiveBaseSchema):
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


class DrillUpdateSchema(DrillArchiveBaseSchema): ...


class DrillDeleteSchema(BaseModel):
    id: int
