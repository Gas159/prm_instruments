from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    id: int | None = None
    name: str
    description: str
    company_id: int | None
    # comment: str | None = None
    # rate: int | None = None

    model_config = ConfigDict(from_attributes=True)


class Service(ServiceBase):
    pass


class CreateService(BaseModel):
    name: str
    description: str
    company_id: int | None
    # comment: str | None = None
    # rate: int | None = None

    model_config = ConfigDict(from_attributes=True)


class DeleteService(Service):
    # msg: str = "Service deleted successfully"
    pass


class ServiceUpdate(ServiceBase):
    name: str | None = None
    description: str | None = None
