from datetime import timedelta

from celery.backends.database import retry

from auth_jwt.jwt_utils import encode_jwt
from auth_jwt.schemas import UserAuthJWTSchema


from config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expires_minutes: int = settings.auth_jwt.access_token_expires_minutes,
    expires_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expires_minutes=expires_minutes,
        expires_timedelta=expires_timedelta,
    )


def create_access_token(user: UserAuthJWTSchema) -> str:
    payload = {
        "id": user.id,
        "sub": user.username,
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "type": ACCESS_TOKEN_TYPE,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expires_minutes=settings.auth_jwt.access_token_expires_minutes,
    )


def create_refresh_token(user: UserAuthJWTSchema) -> str:
    payload = {
        "id": user.id,
        "sub": user.username,
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "type": REFRESH_TOKEN_TYPE,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expires_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expires_days),
    )