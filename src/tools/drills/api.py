import logging
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy import and_

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import db_helper
from tools.drills.models import DrillModel
from tools.drills.schemas import (
    DrillSchema,
    DrillCreateSchema,
    DrillUpdateSchema,
)
from tools.drills.cruds import add_drill, update_drill_in_db, delete_drill_from_bd

router = APIRouter()


loger = logging.getLogger(__name__)


# Get ONE
@router.get("/{tool_id}", response_model=DrillSchema)
async def get_one(
    tool_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillModel:

    query = select(DrillModel).where(DrillModel.id == tool_id)
    result = await session.execute(query)
    tool = result.scalars().first()
    loger.info("Get tool: %s", tool)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


# Get ALL
@router.get("", response_model=List[DrillSchema])
async def get_all(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    broken: bool | None = Query(False),
    diameter: List[float] | None = Query(None),  # Получение списка выбранных диаметров
) -> List[DrillModel]:

    loger.debug("Get tools: %s", broken)

    query = select(DrillModel)
    # Применение фильтров, если они заданы
    filters = []
    if broken is not None:
        loger.debug("Check broken: %s", broken)
        filters.append(DrillModel.is_broken == broken)
    #
    if diameter is not None:
        loger.debug("Check diameter: %s", diameter)
        filters.append(DrillModel.diameter.in_(diameter))

    # Применение фильтров к запросу
    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query)
    drills = result.scalars().all()
    # Преобразование SQLAlchemy моделей в Pydantic
    return list(drills)


@router.post("/create/")
async def create_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill: Annotated[DrillCreateSchema, Depends()],
) -> DrillSchema:
    loger.info("Create tool: %s", drill)

    result = await add_drill(session, drill)
    return result


@router.put("/update/{tool_id}", response_model=DrillSchema)
async def update_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_id: int,
    drill: DrillUpdateSchema,
) -> DrillModel:
    loger.info("Update tool: %s", drill)

    result = await update_drill_in_db(session, drill_id, drill)
    return result


#
#
# # Обновление статуса состояния инструмента
# @router.post("/update_broken_status/{tool_id}")
# async def update_tool_status(
#     tool_id: int,
#     request: Request,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ):
#     loger.info("Update tool status: %s", tool_id)
#     data = await request.json()
#     is_broken = data.get("is_broken")
#
#     # Получаем инструмент по ID
#     tool = await session.get(ToolModel, tool_id)
#     if not tool:
#         return JSONResponse(status_code=404, content={"message": "Tool not found"})
#
#     # Обновляем статус
#     tool.is_broken = is_broken
#     await session.commit()
#     loger.info("Tool status updated successfully")
#     return {"message": "Tool status updated successfully"}
#
#
# Удаление сверла
@router.delete("/delete/{tool_id}", response_model=DrillSchema)
async def delete_drill(
    drill_id: int, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> DrillSchema:
    result = await delete_drill_from_bd(session, drill_id)
    return result
