
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy


cookie_transport = CookieTransport(cookie_name="car_service", cookie_max_age=3600)


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


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
