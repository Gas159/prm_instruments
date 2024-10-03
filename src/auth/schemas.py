from datetime import datetime

from fastapi_users import schemas
from fastapi_users.schemas import model_dump
from pydantic import EmailStr, ConfigDict, Field, BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str | None = None
    role: str | None = None
    registration_at: datetime

    model_config = ConfigDict(from_attributes=True)

    # second_name: str


class UserCreate(schemas.BaseUserCreate):
    # class UserCreate(BaseModel):
    email: EmailStr = Field(
        examples=["test@example.com"], default="test@example.com", max_length=320
    )
    password: str = Field(default="123", max_length=128)
    name: str | None = Field(examples=["test"], default="test", max_length=32)
    # second_name: str | None = Field(
    #     examples=["1second_name1"], default="second_name", max_length=32
    # )
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
