from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy


cookie_transport = CookieTransport(
    cookie_name="parma_access",
    cookie_max_age=36000,
    # cookie_secure=False,
    cookie_httponly=True,
    cookie_samesite="none",
)


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=36000)


# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=cookie_transport,
#     get_strategy=get_jwt_strategy,
# )
#
# fastapi_users = FastAPIUsers[UserModel, int](
#     get_user_manager,
#     [auth_backend],
# )
#
# current_active_user = fastapi_users.current_user(active=True)
