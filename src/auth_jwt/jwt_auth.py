import logging

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from auth_jwt.jwt_utils import hash_password, encode_jwt, validate_password, decode_jwt
from auth_jwt.schemas import UserAuthJWTSchema, TokenInfo
from loggind_config import setup_logging
from tools.drills.cruds import logger

# setup_logging()
# logger = logging.getLogger(__name__)

http_bearer = HTTPBearer()

router = APIRouter(prefix="/auth_jwt", tags=["JWT"])


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


def get_current_token_payload(
    # token: str = Depends(http_bearer),  # читаем токен из заголовка, возрващает scheme='Bearer' credentials='123
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),  # читаем токен из заголовка
) -> UserAuthJWTSchema:

    logger.debug("Token: %s", credentials)  # {'scheme': 'Bearer', 'credentials': '123'}
    token = credentials.credentials
    logger.debug("Token: %s", token)  # 123 - access token
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}")
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserAuthJWTSchema:
    username: str | None = payload.get("sub")
    if not (user := user_db.get(username)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found, token invalid")
    return user


def get_current_active_auth_user(
    user: UserAuthJWTSchema = Depends(get_current_auth_user),
):
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


@router.post("/login", response_model=TokenInfo)
def auth_user_login_jwt(
    user: UserAuthJWTSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "id": user.id,
        "sub": user.username,
        "username": user.username,
        "email": user.email,
        "active": user.active,
    }
    token = encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "Bearer"}


@router.get("/users/me")
def auth_user_check_self_info(
    user: UserAuthJWTSchema = Depends(get_current_active_auth_user),
    payload: dict = Depends(get_current_token_payload),
):
    iat = payload.get("iat")
    return user, {"logged_in_at": iat, "username": user.username, "email": user.email, "active": user.active}
    # return user
