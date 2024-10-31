from aiofiles.os import access
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError

from auth_jwt.helpers import (
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    REFRESH_TOKEN_TYPE,
)
from auth_jwt.jwt_utils import hash_password, validate_password, decode_jwt
from auth_jwt.schemas import UserAuthJWTSchema, TokenInfoSchema

from tools.drills.cruds import logger


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_jwt/login")

router = APIRouter(
    prefix="/auth_jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


john = UserAuthJWTSchema(
    id=1,
    username="john",
    password=hash_password("qwerty"),
    active=True,
    email="j111@1111j.com",
)

sam = UserAuthJWTSchema(
    id=2,
    username="sam",
    password=hash_password("qwerty123"),
    active=True,
    email="s2222@s2222.com",
)


user_db: dict[str, UserAuthJWTSchema] = {
    john.username: john,
    sam.username: sam,
}


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
) -> UserAuthJWTSchema:
    # logger.debug("Token: %s", credentials)  # {'scheme': 'Bearer', 'credentials': '123'}
    # token = credentials.credentials
    logger.debug("Token: %s, type: %s", token, token)  # 123 - access token
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}")
    return payload


def get_user_by_token_sub(payload: dict) -> UserAuthJWTSchema:
    username: str | None = payload.get("sub")
    if not (user := user_db.get(username)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found, token invalid")
    return user


def get_auth_user_from_token_of_type(token_type: str):  # 1
    def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload)) -> UserAuthJWTSchema:

        validate_token_type(payload=payload, token_type=token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: dict = Depends(get_current_token_payload)) -> UserAuthJWTSchema:
        validate_token_type(payload=payload, token_type=self.token_type)
        return get_user_by_token_sub(payload)


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserAuthJWTSchema = Depends(get_current_auth_user),
) -> UserAuthJWTSchema:
    if user.active:
        return user
    logger.debug("User is not active: %s", user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")


def validate_auth_user(
    username: str = Form("john"),
    password: str = Form("qwerty"),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if not (user := user_db.get(username)):
        raise unauthed_exc
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user
