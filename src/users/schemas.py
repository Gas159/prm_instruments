from pydantic import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    name: str
    # second_name: str
    email: str | None
    # foo: str
    # bar: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserCreate(UserBase):
    pass


# class UserGetOne(UserRead):
#     pass
