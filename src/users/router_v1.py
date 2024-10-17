import json
import logging
from typing import Annotated


from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import db_helper
from users import cruds as users_crud
from users.models import RoleModel, UserModel
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
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserSchema:

    query = select(UserModel).where(UserModel.id == user_id).options(selectinload(UserModel.roles))
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    logger.info("Get user: %s", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.model_validate(user)


# @router.get("/{tool_id}", response_model=DrillSchema)
# async def get_one(
#     tool_id: int,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ) -> DrillSchema:
#
#     query = (
#         select(DrillModel)
#         .where(DrillModel.id == tool_id)
#         .options(selectinload(DrillModel.plates), selectinload(DrillModel.screws))
#     )
#     result = await session.execute(query)
#     tool = result.scalars().first()
#     logger.info("Get tool: %s", tool)
#     if not tool:
#         raise HTTPException(status_code=404, detail="Tool not found")
#     return DrillSchema.model_validate(tool)


@router.get("/users", response_model=list[UserSchema])
async def get_all_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[UserSchema]:
    users = await users_crud.get_all_users(session=session)
    return [UserSchema.model_validate(user) for user in users]


# Присвоение роли пользователю
@router.post("/users/{user_id}/roles/{role_id}/", response_model=UserSchema)
async def assign_role_to_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    role_id: int,
):
    db_user = await session.get(UserModel, user_id, options=[selectinload(UserModel.roles)])
    role_db = await session.execute(select(RoleModel).where(RoleModel.id == role_id))
    role = role_db.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Проверяем, есть ли уже эта роль у пользователя
    if role in db_user.roles:
        raise HTTPException(status_code=400, detail="User already has this role")

    db_user.roles.append(role)
    await session.commit()
    # await session.refresh(db_user, attribute_names=["roles"])
    await session.refresh(db_user)
    logger.info("Updated user roles: %s", db_user.roles)
    return db_user


@router.get("/roles", response_model=list[RoleSchema])
async def get_roles(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[RoleSchema]:
    query = select(RoleModel).options(selectinload(RoleModel.users))
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
