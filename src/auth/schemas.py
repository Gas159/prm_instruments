from datetime import datetime

from fastapi_users import schemas
from fastapi_users.schemas import model_dump
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
    email: EmailStr = Field(
        examples=["j1Cw5Z@example.com"], default="jCw5Z@example.com", max_length=320
    )
    password: str = Field(default="VeryStrongPassword123!!!", max_length=128)
    username: str | None = Field(
        examples=["1first_name1"], default="first_name", max_length=32
    )
    second_name: str | None = Field(
        examples=["1second_name1"], default="second_name", max_length=32
    )
    # role_id: int
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str  # EmailStr
    password: str

    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(schemas.BaseUserUpdate):
    pass
