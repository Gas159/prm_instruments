from pydantic import BaseModel, ConfigDict, EmailStr


class UserAuthJWTSchema(BaseModel):
    model_config = ConfigDict(strict=True)  # указывает типы данных строго

    id: int
    username: str
    password: bytes
    active: bool = True
    email: EmailStr | None = None


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
