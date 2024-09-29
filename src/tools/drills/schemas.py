from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DrillBaseSchema(BaseModel):
    name: str
    diameter: float | None
    length: float | None
    deep_of_drill: float | None
    plate: str | None
    screws: str | None
    key: str | None
    company: str | None
    is_broken: bool | None
    image_path: str | None
    storage: str | None
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DrillSchema(DrillBaseSchema):
    # services: list[Service] = []
    id: int


class DrillCreateSchema(BaseModel):
    name: str
    diameter: float
    length: float | None = None
    deep_of_drill: float
    plate: str | None = None
    screws: str | None = None
    key: str | None = None
    company: str | None = None
    storage: str | None = "Склад"
    image_path: str | None = None
    is_broken: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class DrillUpdateSchema(DrillCreateSchema): ...


class DrillDeleteSchema(BaseModel):
    id: int
