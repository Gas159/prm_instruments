import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth_jwt.helpers import create_access_token, create_refresh_token
from auth_jwt.jwt_auth import (
    http_bearer,
    validate_auth_user,
    get_current_active_auth_user,
    get_current_auth_user_for_refresh,
)
from auth_jwt.jwt_utils import hash_password
from auth_jwt.schemas import TokenInfoSchema
from database import db_helper
from users.helpers import role_checker
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
        raise HTTPException(status_code=400, detail="Email already exists")
    logger.debug("result: %s", user)

    logger.debug("user.phone_number: %s", user.phone_number)
    if user.phone_number:
        if user.phone_number == "911":
            user.phone_number = None
        else:
            query = select(UserModel).where(UserModel.phone_number == user.phone_number)
            result = await session.execute(query)
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise HTTPException(status_code=400, detail="Phone number already exists")

    hashed_password = hash_password(user.password).decode("utf-8")

    new_user = UserModel(
        **user.model_dump(exclude={"password"}, exclude_none=True, exclude_unset=True),
        hashed_password=hashed_password,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Предзагрузка связанных данных
    query = select(UserModel).where(UserModel.id == new_user.id).options(selectinload(UserModel.roles))
    result = await session.execute(query)
    new_user_with_roles = result.scalar_one()
    return UserSchema.model_validate(new_user_with_roles)


@router.post("/login", response_model=TokenInfoSchema, response_model_exclude_none=True)
def auth_user_login_jwt(
    response: Response,
    user: UserSchema = Depends(validate_auth_user),
):
    logger.debug("Заход в  логин. User: %s", user)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie(
        key="parma_refresh",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        max_age=60 * 60 * 24 * 7,  # 7 days
        # max_age=45 # 45 seconds
    )
    return TokenInfoSchema(access_token=access_token, token_type="Bearer")  # refresh_token=refresh_token,


@router.post("/logout/")
def logout_user(response: Response):
    response.delete_cookie(key="parma_refresh")
    return {"message": "Пользователь успешно вышел из системы"}


@router.post("/refresh", response_model_exclude_none=True)
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
    # user: UserAuthJWTSchema =Depends( get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    # user: UserAuthJWTSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
) -> dict:
    access_token = create_access_token(user)
    # return TokenInfoSchema(access_token=access_token)
    user_data = UserSchema.model_validate(user)
    return {"access_token": access_token, "user": user_data}


@router.get("/users/me", response_model=UserSchema)
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user),
    # payload: dict = Depends(get_current_token_payload),
):
    return user


@router.get("/check/read")
async def check_read(_: None = Depends(role_checker(["admin", "user"]))):
    return {"message": "You have access to read"}


@router.get("/check/write")
async def check_write(fds: UserSchema):
    return {"message": "You have access to write"}
