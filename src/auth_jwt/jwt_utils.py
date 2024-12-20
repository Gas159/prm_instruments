import logging
import uuid
from datetime import datetime, timezone, timedelta

from jwt import InvalidSignatureError
from jwt.exceptions import InvalidTokenError
import bcrypt
import jwt
from config import settings

logger = logging.getLogger(__name__)


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expires_minutes: int = settings.auth_jwt.access_token_expires_minutes,
    expires_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expires_timedelta:
        expire = now + expires_timedelta
    else:
        expire = now + timedelta(minutes=expires_minutes)
    logger.debug("expire: %s", expire)

    to_encode.update(
        {
            "exp": expire,
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
    )
    logger.debug("Final payload for JWT encoding: %s", to_encode)
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    except InvalidSignatureError as e:
        raise InvalidTokenError(f"invalid signature error: {e}")
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(password=pwd_bytes, hashed_password=hashed_password)
