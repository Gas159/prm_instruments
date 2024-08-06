from pydantic import BaseModel, ConfigDict


class Service(BaseModel):
    name: str
    description: str

    # class Config:
    # 	orm_mode = True


class GetOneService(Service):
    model_config = ConfigDict(from_attributes=True)
    id: int



class GetAllService(GetOneService):
    pass


class CreateService(Service):
    pass
