from pydantic import BaseModel, ConfigDict


class SToolBase(BaseModel):
    name: str
    diameter: float | None = None
    length: float | None = None
    deep_of_drill: float | None = None
    plate: str | None = None
    screws: str | None = None
    key: str | None = None
    company: str | None = None
    is_broken: bool | None = None

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
