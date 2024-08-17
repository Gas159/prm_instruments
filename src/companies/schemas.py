from pydantic import BaseModel, ConfigDict
from services.schemas import Service


class SCompanyBase(BaseModel):
    id: int | None = None
    name: str
    description: str
    coordinates: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SCompany(SCompanyBase):
    services: list[Service] = []

    # class Config:
    #     fields = {
    #         'id': {'alias': 'id'},
    #     }


class SCompanyCreate(BaseModel):
    name: str
    description: str
    coordinates: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SCompanyDelete(SCompanyBase):
    # msg: str = "Service deleted successfully"
    pass


class SCompanyUpdate(SCompanyBase):
    name: str | None = None
    description: str | None = None
