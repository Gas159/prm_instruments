from pydantic import BaseModel, ConfigDict


from schemas.service import Service


class SCompanyBase(BaseModel):
    name: str
    description: str
    coordinates: list | None
    services: list[Service] = []

    # msg: str | None = None
    model_config = ConfigDict(from_attributes=True)




class SCompany(SCompanyBase):
    # model_config = ConfigDict(from_attributes=True)
    id: int


class SCompanyCreate(SCompanyBase):
    # msg: str = "Service created successfully"
    services: int
    pass


class SCompanyDelete(SCompanyBase):
    # msg: str = "Service deleted successfully"
    services: list[Service] = []
    pass


class SCompanyUpdate(SCompanyBase):
    name: str | None = None
    description: str | None = None
