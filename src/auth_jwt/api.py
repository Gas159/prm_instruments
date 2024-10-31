import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_jwt.helpers import create_access_token, create_refresh_token
from auth_jwt.jwt_auth import (
    http_bearer,
    validate_auth_user,
    get_current_active_auth_user,
    get_current_auth_user_for_refresh,
)
from auth_jwt.jwt_utils import hash_password
from auth_jwt.schemas import UserAuthJWTSchema, TokenInfoSchema
from database import db_helper
from users.models import UserModel
from users.schemas import UserRegisterSchema, UserSchema

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/auth_jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register", response_model=UserSchema)
async def auth_user_register(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: UserRegisterSchema,
):

    query = select(UserModel).where(UserModel.email == user.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    logger.debug("result: %s", user)

    hashed_password = hash_password(user.password).decode("utf-8")
    new_user = UserModel(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserSchema.model_validate(new_user)


@router.post("/login", response_model=TokenInfoSchema)
def auth_user_login_jwt(
    user: UserAuthJWTSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfoSchema(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")


@router.post("/refresh", response_model=TokenInfoSchema, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
    # user: UserAuthJWTSchema =Depends( get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    # user: UserAuthJWTSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
) -> TokenInfoSchema:
    access_token = create_access_token(user)
    return TokenInfoSchema(access_token=access_token)


@router.get("/users/me")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user),
    # payload: dict = Depends(get_current_token_payload),
):
    return user
