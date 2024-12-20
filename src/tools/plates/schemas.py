from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, model_serializer, Field
from enum import Enum


class MaterialEnum(str, Enum):
    P = "P"
    M = "M"
    K = "K"
    N = "N"
    S = "S"
    H = "H"


# Базовая схема для пластин
class PlateBaseSchema(BaseModel):
    type: str | None = None
    sub_type: str | None = None
    # material: MaterialEnum | None = Field(None, description="Available options: P, M, K, N, S, H")
    material: str | None = None
    amount: int | None = None
    min_amount: int | None = None
    company: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


# Схема для отображения полной информации о пластине
class PlateSchema(PlateBaseSchema):
    id: int | None = None
    image_path: str | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_serializer
    def model_serializer(self):
        return {
            "id": self.id,
            "type": self.type,
            "sub_type": self.sub_type,
            "material": self.material,
            "amount": self.amount,
            "min_amount": self.min_amount,
            "company": self.company,
            "image_path": self.image_path,
            "description": self.description,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }


class PlateCreateSchema(PlateBaseSchema):
    pass


class PlateUpdateSchema(PlateBaseSchema):
    pass


class PlateDeleteSchema(BaseModel):
    id: int
