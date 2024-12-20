import logging
from datetime import timedelta
from auth_jwt.jwt_utils import encode_jwt
from config import settings
from users.schemas import UserSchema


logger = logging.getLogger(__name__)

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


def create_access_token(user: UserSchema) -> str:
    payload = {
        "id": user.id,
        "sub": user.first_name,
        "username": user.last_name,
        "email": user.email,
        "active": user.is_active,
        "type": ACCESS_TOKEN_TYPE,
        "roles": [role.model_dump() for role in user.roles],
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expires_minutes=settings.auth_jwt.access_token_expires_minutes,
    )


def create_refresh_token(user: UserSchema) -> str:
    payload = {
        "id": user.id,
        "sub": user.first_name,
        "username": user.last_name,
        "email": user.email,
        "active": user.is_active,
        "type": REFRESH_TOKEN_TYPE,
        "roles": [{"id": role.id, "role": role.role} for role in user.roles],
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        # expires_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expires_days),
        expires_minutes=settings.auth_jwt.refresh_token_expires_minutes,
    )
