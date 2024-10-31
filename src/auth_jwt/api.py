from fastapi import APIRouter, Depends

from auth_jwt.helpers import create_access_token, create_refresh_token, REFRESH_TOKEN_TYPE
from auth_jwt.jwt_auth import (
    http_bearer,
    validate_auth_user,
    get_current_token_payload,
    get_current_active_auth_user,
    get_current_auth_user_for_refresh,
    get_auth_user_from_token_of_type,
    UserGetterFromToken,
)
from auth_jwt.schemas import UserAuthJWTSchema, TokenInfoSchema

router = APIRouter(
    prefix="/auth_jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/login", response_model=TokenInfoSchema)
def auth_user_login_jwt(
    user: UserAuthJWTSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfoSchema(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")


@router.post("/refresh", response_model=TokenInfoSchema, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: UserAuthJWTSchema = Depends(get_current_auth_user_for_refresh),
    # user: UserAuthJWTSchema =Depends( get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    # user: UserAuthJWTSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
) -> TokenInfoSchema:
    access_token = create_access_token(user)
    return TokenInfoSchema(access_token=access_token)


@router.get("/users/me")
def auth_user_check_self_info(
    user: UserAuthJWTSchema = Depends(get_current_active_auth_user),
    payload: dict = Depends(get_current_token_payload),
):
    return user, payload