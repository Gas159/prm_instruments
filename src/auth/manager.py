from typing import Optional, Annotated
from fastapi import Depends, Request, Response
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    FastAPIUsers,
)
from fastapi_users.authentication import AuthenticationBackend

from auth.auth import cookie_transport, get_jwt_strategy
from auth.database import get_user_db
from auth.schemas import UserCreate
from auth.models import User
from project_services.task_celery.tasks import send_email_test

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    user_db_model = User  # Модель пользователя

    async def create(
        self,
        user_create: Annotated[UserCreate, Depends()],
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        # Устанавливаем поля по умолчанию
        # user_dict["is_active"] = True
        # user_dict["is_superuser"] = False
        # user_dict["is_verified"] = False

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")
        # send_email_test(
        #     name=user.name,
        #     email_to_send=user.email,
        #     msg="Вы зарегистрированы. Это точно, наверное, ну максимум - нет:)",
        # )

    # async def on_after_login(self, user: User):
    #     print(f"User {user} has login.")
    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        print(f"User {user.name} has login.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
