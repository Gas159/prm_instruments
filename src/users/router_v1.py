import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from users import cruds as users_crud
from users.models import RoleModel
from users.schemas import RoleSchema, UserSchema, RoleCreateSchema

router = APIRouter(
    # prefix=settings.api.v1.users,
    # tags=["users"],
    # responses={404: {"description": "Not found"}}
)
logger = logging.getLogger(__name__)


@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserSchema:
    user = await users_crud.get_user(session=session, user_id=user_id)
    return UserSchema.model_validate(user)


@router.get("/users", response_model=list[UserSchema])
async def get_all_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[UserSchema]:
    users = await users_crud.get_all_users(session=session)
    return [UserSchema.model_validate(user) for user in users]


@router.get("/roles", response_model=list[RoleSchema])
async def get_roles(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[RoleSchema]:
    query = select(RoleModel)
    result = await session.execute(query)
    roles = result.scalars().all()
    logger.info("Get roles: %s %s", type(roles), roles)
    return [RoleSchema.model_validate(role) for role in roles]
    # return roles


@router.post("/role", response_model=RoleSchema)
async def create_role(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    role: RoleCreateSchema | str = Form(...),
) -> RoleSchema:
    try:
        logger.info("Role: %s %s", type(role), role)
        role_data = json.loads(role)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format" + str(e))

    result = await session.execute(select(RoleModel).filter_by(role=role_data["role"]))
    existing_role = result.scalars().first()

    if existing_role:
        raise HTTPException(status_code=400, detail=f"Role '{role_data['role']}' already exists.")

    role = RoleModel(**role_data)
    session.add(role)
    await session.commit()
    await session.refresh(role)
    role_dict = {"id": role.id, "role": role.role}

    return RoleSchema.model_validate(role_dict)


@router.delete("/role/{role_id}", response_model=RoleSchema)
async def delete_role(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    role_id: int,
) -> RoleSchema:
    query = select(RoleModel).where(RoleModel.id == role_id)
    role = await session.execute(query)
    role_for_del = role.scalar_one_or_none()

    if role_for_del is None:
        raise HTTPException(status_code=404, detail="Role not found")
    await session.delete(role_for_del)
    await session.commit()
    logger.info("Delete drills: %s %s", role_for_del, role_for_del.__dict__.items())
    return RoleSchema.model_validate(role_for_del)
