import logging
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import db_helper
from tools.archive.drills.models import DrillArchiveModel
from tools.archive.drills.schemas import DrillArchiveSchema

router = APIRouter()


logger = logging.getLogger(__name__)


# Get ONE
@router.get("/drill_archive/{tool_id}", response_model=DrillArchiveSchema)
async def get_one(
    tool_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillArchiveModel:

    query = select(DrillArchiveModel).where(DrillArchiveModel.id == tool_id)
    logger.info("query: %s", query)
    result = await session.execute(query)
    logger.info("result: %s", result)
    tool = result.scalar()
    logger.info("Get tool: %s", tool)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


# Get ALL
@router.get("/drills_archive", response_model=List[DrillArchiveSchema])
async def get_all(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    broken: bool | None = Query(False),
    diameter: List[float] | None = Query(None),  # Получение списка выбранных диаметров
) -> List[DrillArchiveModel]:

    logger.debug("Get tools: %s", broken)

    query = select(DrillArchiveModel)
    # Применение фильтров, если они заданы
    filters = []
    if broken is not None:
        logger.debug("Check broken: %s", broken)
        filters.append(DrillArchiveModel.is_broken == broken)
    #
    if diameter is not None:
        logger.debug("Check diameter: %s", diameter)
        filters.append(DrillArchiveModel.diameter.in_(diameter))

    # Применение фильтров к запросу
    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query)
    drills = result.scalars().all()
    # Преобразование SQLAlchemy моделей в Pydantic
    return list(drills)
