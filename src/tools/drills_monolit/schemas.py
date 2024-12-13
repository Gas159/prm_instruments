from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_serializer


class DrillMonolitBaseSchema(BaseModel):
    material: str | None = None
    name: str | None = None
    diameter: float | None = None
    length_xD: float | None = None
    deep_of_drill: float | None = None
    coating: str | None = None
    count: int | None = None
    count_min: int | None = None
    company: str | None = None
    storage: str | None = "Склад"
    is_broken: bool | None = False
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DrillMonolitSchema(DrillMonolitBaseSchema):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    id: int
    image_path: str | None = None
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "id": self.id,
            "material": self.material,
            "name": self.name,
            "diameter": self.diameter,
            "length_xD": self.length_xD,
            "deep_of_drill": self.deep_of_drill,
            "coating": self.coating,
            "count": self.count,
            "count_min": self.count_min,
            "company": self.company,
            "storage": self.storage,
            "is_broken": self.is_broken,
            "description": self.description,
            "image_path": self.image_path,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }


class DrillMonolitCreateSchema(DrillMonolitBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    ...


class DrillMonolitUpdateSchema(DrillMonolitBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    ...


class DrillMonolitDeleteSchema(BaseModel):
    id: int
