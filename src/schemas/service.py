from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    description: str
    company_id: int | None
    comment: str | None = None
    rate: int | None = None
    # msg: str | None = None
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True


class Service(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CreateService(Service):
    # msg: str = "Service created successfully"
    pass


class DeleteService(Service):
    # msg: str = "Service deleted successfully"
    pass


class ServiceUpdate(ServiceBase):
    name: str | None = None
    description: str | None = None
