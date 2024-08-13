from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, BaseModel


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
    username: str
    second_name: str
    email: EmailStr
    password: str
    # role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
