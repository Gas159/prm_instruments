import logging

from fastapi import Depends, HTTPException

from auth_jwt.jwt_auth import get_current_active_auth_user
from users.schemas import UserSchema


logger = logging.getLogger(__name__)


def role_checker(required_roles: list[str]):
    async def check_user_role(user: UserSchema = Depends(get_current_active_auth_user)) -> None:

        user_roles = [role.role for role in user.roles]
        # if not any( role in user_roles  for role in required_roles):
        if not [role for role in required_roles if role in user_roles]:
            raise HTTPException(
                status_code=403,
                detail=f"""You don't have access to this resource.
                       Required: {' '.join(required_roles)!r}, current: {', '.join( user_roles)!r}""",
            )

    return check_user_role
