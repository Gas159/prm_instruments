from datetime import datetime

# from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, model_serializer

# if TYPE_CHECKING:
#     from tools.drills.schemas import DrillSchema

# from tools.drills.schemas import DrillSchema
# from tools.schemas_type import ScrewSchemaType, PlateSchemaType
# from tools.dsa import DrillSchemaType


class ScrewBaseSchema(BaseModel):
    type: str | None = None
    length: float | None = None
    thread: str | None = None
    step_of_thread: float | None = None
    company: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ScrewSchema(ScrewBaseSchema):
    id: int | None = None

    image_path: str | None = None
    # drills: List["DrillSchema"] | None = None

    create_at: datetime | None = None
    update_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

    # @model_serializer
    # def custom_serializer(self):
    #     # Возвращаем поля в нужном порядке
    #     return {
    #         "id": self.id,
    #         "type": self.type,
    #         "length": self.length,
    #         "thread": self.thread,
    #         "step_of_thread": self.step_of_thread,
    #         "company": self.company,
    #         "description": self.description,
    #         "image_path": self.image_path,
    #         "create_at": self.create_at,
    #         "update_at": self.update_at,
    #     }


class ScrewCreateSchema(ScrewBaseSchema):

    model_config = ConfigDict(from_attributes=True)


class ScrewUpdateSchema(ScrewBaseSchema): ...


class ScrewDeleteSchema(BaseModel):
    id: int
