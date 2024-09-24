from pydantic import BaseModel, ConfigDict


class SToolBase(BaseModel):
    name: str
    diameter: float | None
    length: float | None
    deep_of_drill: float | None
    plate: str | None
    screws: str | None
    key: str | None
    company: str | None
    is_broken: bool | None

    model_config = ConfigDict(from_attributes=True)


class STool(SToolBase):
    # services: list[Service] = []
    id: int


class SToolCreate(SToolBase):
    pass


class SToolUpdate(SToolBase):

    model_config = ConfigDict(from_attributes=True)


class SDeleteTool(BaseModel):
    id: int
