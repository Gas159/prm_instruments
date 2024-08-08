from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    description: str

    # class Config:
    # 	orm_mode = True


class Service(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CreateService(ServiceBase):
    pass


# class GetAllService(ServiceBaseRead):
#     pass
