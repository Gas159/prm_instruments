from datetime import datetime

from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, Field, BaseModel


class UserRead(schemas.BaseUser[int]):
    # class UserRead(BaseModel):
    id: int
    # id: models.ID
    username: str
    second_name: str
    email: str  # EmailStr
    registration_at: datetime
    # is_active: bool = True
    # is_superuser: bool = False
    # is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
# class UserCreate(BaseModel):
    # class UserCreate(BaseModel):
    username: str | None = Field(default="first_name", max_length=32)
    second_name: str | None = Field(default="second_name", max_length=32)
    # email: EmailStr
    # password: str | None = Field(default="password", max_length=128)
    # role_id: int
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False


    model_config = ConfigDict(from_attributes=True)


class UserUpdate(schemas.BaseUserUpdate):
    pass
