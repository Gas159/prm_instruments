from datetime import datetime

from pydantic import BaseModel, model_serializer, Field, EmailStr
from pydantic import ConfigDict
from sqlalchemy import func, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped


class RoleBaseSchema(BaseModel):
    role: str
    model_config = ConfigDict(from_attributes=True)


class RoleSchema(RoleBaseSchema):
    id: int
    role: str

    @model_serializer
    def custom_serializer(self) -> dict:
        return {"id": self.id, "role": self.role}


class RoleCreateSchema(RoleBaseSchema):
    pass


class UserBaseSchema(BaseModel):
    name: str
    second_name: str | None
    email: str | None
    model_config = ConfigDict(from_attributes=True)


class UserRegisterSchema(UserBaseSchema):
    name: str | None = Field(examples=["first"], default="first", max_length=32)
    second_name: str | None = Field(examples=["second"], default="second", max_length=32)
    email: EmailStr = Field(examples=["test@example.com"], default="test@example.com", max_length=320)
    password: str = Field(default="123", max_length=128)


class UserSchema(UserBaseSchema):
    id: int
    name: str | None = None
    second_name: str | None = None
    email: EmailStr
    # roles: list["RoleSchema"] | None = []
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    registration_at: datetime

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "second_name": self.second_name,
            "email": self.email,
            # "roles": self.roles,
            "registration_at": self.registration_at,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
        }


class UserCreateSchema(UserBaseSchema):
    pass
