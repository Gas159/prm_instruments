from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    description: str
    # msg: str | None = None

    # class Config:
    # 	orm_mode = True


class Service(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CreateService(ServiceBase):
    # msg: str = "Service created successfully"
    pass


class DeleteService(Service):
    # msg: str = "Service deleted successfully"
    pass


class ServiceUpdate(ServiceBase):
    name: str | None = None
    description: str | None = None
