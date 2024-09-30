from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DrillBaseSchema(BaseModel):
    name: str
    diameter: float | None
    length_xD: float | None
    deep_of_drill: float | None
    plate: str | None = "?"
    screw: str | None = "?"
    key: str | None = "?"
    company: str | None = "?"
    is_broken: bool | None = False
    # image_path: str | None
    storage: str | None = "Склад"
    description: str | None = "?"

    model_config = ConfigDict(from_attributes=True)


class DrillSchema(DrillBaseSchema):
    # services: list[Service] = []
    id: int
    image_path: str | None

    create_at: datetime
    update_at: datetime


class DrillCreateSchema(DrillBaseSchema):
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


class DrillUpdateSchema(DrillBaseSchema): ...


class DrillDeleteSchema(BaseModel):
    id: int
