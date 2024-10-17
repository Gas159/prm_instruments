from pydantic import BaseModel, model_serializer
from pydantic import ConfigDict


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
    roles: list["RoleSchema"] | None = None
    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserBaseSchema):
    id: int

    @model_serializer
    def custom_serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "second_name": self.second_name,
            "email": self.email,
            "roles": self.roles,
        }


class UserCreateSchema(UserBaseSchema):
    pass
