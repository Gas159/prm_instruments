import logging
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, Query, UploadFile, File, Form
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import db_helper
from tools.drills.cruds import add_drill, update_drill_in_db, delete_drill_from_bd
from tools.drills.models import DrillModel
from tools.drills.schemas import (
    DrillSchema,
    DrillCreateSchema,
    DrillUpdateSchema,
)

router = APIRouter()


logger = logging.getLogger(__name__)


# Get ONE


@router.get("/{tool_id}", response_model=DrillSchema)
async def get_one(
    tool_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillSchema:

    query = (
        select(DrillModel)
        .where(DrillModel.id == tool_id)
        .options(selectinload(DrillModel.plates), selectinload(DrillModel.screws))
    )
    result = await session.execute(query)
    tool = result.scalars().first()
    logger.info("Get tool: %s", tool)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


# Get ALL


@router.get("s", response_model=List[DrillSchema])
async def get_all(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    broken: bool | None = Query(False),
    diameter: List[float] | None = Query(None),  # Получение списка выбранных диаметров
) -> List[DrillSchema]:

    logger.debug("Get tools: %s", broken)

    query = select(DrillModel).options(
        selectinload(DrillModel.plates), selectinload(DrillModel.screws)
    )
    filters = []
    if broken is not None:
        logger.debug("Check broken: %s", broken)
        filters.append(DrillModel.is_broken == broken)
    #
    if diameter is not None:
        logger.debug("Check diameter: %s", diameter)
        filters.append(DrillModel.diameter.in_(diameter))

    # Применение фильтров к запросу
    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query.order_by(DrillModel.id.desc()))
    drills = result.scalars().all()
    return list(drills)


# Create Drill


@router.post("/create", response_model=DrillSchema)
async def create_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill: DrillCreateSchema | str = Form(...),
    screws_ids: list[str] = None,
    image_1: UploadFile | str = File(None),
    image_2: UploadFile | str = File(None),
    image_3: UploadFile | str = File(None),
    # screws: List[ScrewSchema] = Depends(get_all_crews),
    # screw_ids: list = Query(),
    # images: List[UploadFile] | str = File(None),
    # images: Annotated[UploadFile, File(...)] = None,
    # images: List[UploadFile] = File(None, description="Multiple files as UploadFile"),
    # images: List[UploadFile] | None | str = None,
    # images:  Annotated[list[bytes], File()]
) -> DrillSchema:

    logger.info("Drill: %s %s", type(drill), drill)
    logger.info("Screws_ids: %s %s", type(screws_ids), screws_ids)
    images = [image_1, image_2, image_3]
    logger.info("Images: %s %s", type(images), images)
    result = await add_drill(session, drill, screws_ids, images)
    return result


@router.put("/update/{tool_id}", response_model=DrillSchema)
async def update_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_id: int,
    drill: DrillUpdateSchema,
) -> DrillModel:

    logger.info("Update tool: %s", drill)

    result = await update_drill_in_db(session, drill_id, drill)
    return result


# Удаление сверла
@router.delete("/delete/{tool_id}", response_model=DrillSchema)
async def delete_drill(
    drill_id: int, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> DrillSchema:
    result = await delete_drill_from_bd(session, drill_id)
    return result
