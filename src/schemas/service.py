from pydantic import BaseModel, ConfigDict


class Service(BaseModel):
    name: str
    description: str

    # class Config:
    # 	orm_mode = True


class ServiceRead(Service):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CreateService(Service):
    pass


# class GetAllService(ServiceRead):
#     pass
