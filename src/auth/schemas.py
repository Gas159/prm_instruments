from datetime import datetime

from fastapi_users import schemas
from fastapi_users.schemas import model_dump
from pydantic import EmailStr, ConfigDict, Field, BaseModel, model_serializer

from users.schemas import RoleSchema


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str | None = None
    second_name: str | None = None
    email: EmailStr
    roles: list["RoleSchema"] = []
    registration_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "second_name": self.second_name,
            "email": self.email,
            "roles": self.roles,
            "registration_at": self.registration_at,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
        }


class UserCreate(schemas.BaseUserCreate):
    name: str | None = Field(examples=["test"], default="test", max_length=32)
    second_name: str | None = Field(examples=["second"], default="second", max_length=32)
    email: EmailStr = Field(examples=["test@example.com"], default="test@example.com", max_length=320)
    password: str = Field(default="123", max_length=128)
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
