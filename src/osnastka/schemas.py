from dataclasses import Field

from pydantic import BaseModel, ConfigDict


class SToolBase(BaseModel):
	name: str
	diameter: int | float
	lenght: int | float
	deep_of_drill: int | float

	model_config = ConfigDict(from_attributes=True)


class STool(SToolBase):
	# services: list[Service] = []
	id: int


class SToolCreate(SToolBase):
	model_config = ConfigDict(from_attributes=True)


class SToolUpdate(SToolBase):
	...


class SDeleteTool(BaseModel):
	id: int
