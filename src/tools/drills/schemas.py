from datetime import datetime
from typing import List, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, model_serializer


# if TYPE_CHECKING:
#     from tools.plates.schemas import PlateSchema
# from tools.screws.schemas import ScrewSchema

from tools.screws.schemas import ScrewSchema
from tools.plates.schemas import PlateSchema


class DrillBaseSchema(BaseModel):
    name: str = "test"
    diameter: float | None = 0
    length_xD: float | None = 0
    deep_of_drill: float | None = 0
    plate: str | None = None
    key: str | None = None
    company: str | None = None
    is_broken: bool | None = False
    storage: str | None = "Склад"
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DrillSchema(DrillBaseSchema):
    # services: list[Service] = []
    id: int
    image_path: str | None = None

    create_at: datetime
    update_at: datetime
    screws: List["ScrewSchema"] | None = None
    plates: List["PlateSchema"] | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "length_xD": self.length_xD,
            "deep_of_drill": self.deep_of_drill,
            "plate": self.plate,
            "key": self.key,
            "company": self.company,
            "is_broken": self.is_broken,
            "storage": self.storage,
            "description": self.description,
            "image_path": self.image_path,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "screws": self.screws,
            "plates": self.plates,
        }


class DrillCreateSchema(DrillBaseSchema):
    # screw_ids: List[int] | None = None
    # images: List[UploadFile] | str | None = None

    model_config = ConfigDict(from_attributes=True)


class DrillUpdateSchema(DrillBaseSchema): ...


class DrillDeleteSchema(BaseModel):
    id: int
