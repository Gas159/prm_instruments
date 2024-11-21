import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_jwt.cookies import get_token_from_cookies
from auth_jwt.helpers import (
    ACCESS_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    REFRESH_TOKEN_TYPE,
)
from auth_jwt.jwt_utils import validate_password, decode_jwt
from database import db_helper
from users.models import UserModel
from users.schemas import UserSchema, UserLoginSchema

logger = logging.getLogger(__name__)


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_jwt/login")


router = APIRouter(
    prefix="/auth_jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


# john = UserAuthJWTSchema(
#     id=1,
#     username="john",
#     password=hash_password("qwerty"),
#     active=True,
#     email="j111@1111j.com",
# )
#
# sam = UserAuthJWTSchema(
#     id=2,
#     username="sam",
#     password=hash_password("qwerty123"),
#     active=True,
#     email="s2222@s2222.com",
# )

#
# user_db: dict[str, UserAuthJWTSchema] = {
#     john.username: john,
#     sam.username: sam,
# }


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Token type {current_token_type!r} invalid , expected {token_type!r}",
    )


def get_current_token_payload(
    # token: str = Depends(http_bearer),  # читаем токен из заголовка, возрващает scheme='Bearer' credentials='123
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),  # читаем токен из заголовка
    token: str = Depends(oauth2_scheme),  # читаем токен с помощью OAuth2passwordBearer
) -> dict:
    # logger.debug("Token: %s", credentials)  # {'scheme': 'Bearer', 'credentials': '123'}
    # token = credentials.credentials
    logger.debug("Token: %s, type: %s", type(token), token)  # 123 - access token
    try:
        payload = decode_jwt(token=token)
        logger.debug("payload: %s", payload)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token error: {e}")
    return payload


def get_current_token_payload_from_cookie(
    token: str = Depends(get_token_from_cookies),
) -> dict:
    logger.debug("Token: %s, type: %s", type(token), token)  # 123 - access token
    try:
        payload = decode_jwt(token=token)
        logger.debug("payload: %s", payload)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token error: {e}")
    return payload


async def get_user_by_token_from_bd(
    user_id: int,
    # session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserSchema:
    async for session in db_helper.session_getter():
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        logger.debug("Get user from DB: %s", user)
        return UserSchema.model_validate(user)


async def get_user_by_token_sub(
    payload: dict,
) -> UserSchema:
    user_id: str | None = payload.get("id")
    logger.debug("user_id: %s, type %s", user_id, type(user_id))
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID missing from token payload")
    return await get_user_by_token_from_bd(user_id=int(user_id))


def get_auth_user_from_token_of_type(token_type: str):  # 1
    async def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload)):
        validate_token_type(payload=payload, token_type=token_type)
        return await get_user_by_token_sub(payload=payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(self, payload: dict = Depends(get_current_token_payload_from_cookie)) -> UserSchema:
        validate_token_type(payload=payload, token_type=self.token_type)
        return await get_user_by_token_sub(payload=payload)


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
) -> UserSchema:
    if user.is_active:
        return user
    logger.debug("User is not active: %s", user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")


async def validate_auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    login_data: UserLoginSchema
    # username: str = Form("john"),
    # login_data: OAuth2PasswordRequestForm = Depends()
    # email: str = Form(),
    # password: str = Form(),
) -> UserSchema:
    logger.debug("login_data: %s, %s", login_data.email, login_data.password)

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

    query = select(UserModel).where(UserModel.email == login_data.email)
    result = await session.execute(query)
    user_record = result.scalar_one_or_none()

    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    hashed_password = user_record.hashed_password
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")

    if not validate_password(password=login_data.password, hashed_password=hashed_password):
        raise unauthed_exc

    if not user_record.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return UserSchema.model_validate(user_record)


# test@exa213mple.com
