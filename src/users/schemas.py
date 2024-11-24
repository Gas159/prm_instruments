from datetime import datetime
from typing import List

from pydantic import BaseModel, model_serializer, Field, EmailStr
from pydantic import ConfigDict


class RoleBaseSchema(BaseModel):
    role: str
    model_config = ConfigDict(from_attributes=True)


class RoleSchema(RoleBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

    @model_serializer
    def custom_serializer(self) -> dict:
        return {"id": self.id, "role": self.role}


class RoleCreateSchema(RoleBaseSchema):
    pass


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserRegisterSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = Field(examples=["John"], default="first", max_length=32)
    last_name: str | None = Field(examples=["Dou"], default="second", max_length=32)
    email: EmailStr = Field(examples=["test@example.com"], default="test@example.com", max_length=320)
    position: str | None = Field(examples=["killer"], default="worker", max_length=32)
    phone_number: str | None = Field(examples=["911"], default=None, max_length=15)
    password: str = Field(default="123", max_length=128)


class UserLoginSchema(UserBaseSchema):
    grant_type: str
    email: EmailStr = Field(examples=["test@example.com"], default="test@example.com", max_length=320, description="b")
    password: str = Field(default="123", max_length=128)


class UserSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    position: str | None = None
    phone_number: str | None = None
    roles: List["RoleSchema"] | None = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    registration_at: datetime

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "position": self.position,
            "phone_number": self.phone_number,
            "registration_at": self.registration_at,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "roles": self.roles,
        }


class UserCreateSchema(UserBaseSchema):
    pass
