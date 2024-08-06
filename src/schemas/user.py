from pydantic import BaseModel
from pydantic import ConfigDict


class User(BaseModel):
    username: str
    second_name: str
    foo: str
    bar: str


class UserCreate(User):
    pass


class UserRead(User):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserGetOne(UserRead):
    pass
