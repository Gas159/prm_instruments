import logging
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, Query, UploadFile, File, Form
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# from auth.app import role_checker
from database import db_helper
from loggind_config import setup_logging
from tools.drills.cruds import add_drill, update_drill_in_db, delete_drill_from_bd
from tools.drills.models import DrillModel
from tools.drills.schemas import DrillSchema, DrillCreateSchema

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter()


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
    return DrillSchema.model_validate(tool)


# Get ALL


@router.get(
    "s",
    response_model=List[DrillSchema],
    # dependencies=[Depends(role_checker("admin"))],
    dependencies=[Depends(lambda: role_checker("admin"))],
)
async def get_all(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    broken: bool | None = Query(False),
    diameter: List[float] | None = Query(None),  # Получение списка выбранных диаметров
) -> List[DrillSchema]:

    logger.debug("Get tools: %s", broken)

    query = select(DrillModel).options(selectinload(DrillModel.plates), selectinload(DrillModel.screws))
    filters = []
    if broken is not None:
        logger.debug("Check broken: %s", broken)
        filters.append(DrillModel.is_broken == broken)

    if diameter is not None:
        logger.debug("Check diameter: %s", diameter)
        filters.append(DrillModel.diameter.in_(diameter))

    # Применение фильтров к запросу
    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query.order_by(DrillModel.id.desc()))
    drills = result.scalars().all()
    validated_drills = [DrillSchema.model_validate(drill) for drill in drills]
    return validated_drills


# Create Drill


@router.post("/create", response_model=DrillSchema)
async def create_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill: DrillCreateSchema | str = Form(...),
    screws_ids: list[str] = Form([]),
    plates_ids: list[str] = Form([]),
    images: list[UploadFile] = File([]),
) -> DrillSchema:

    logger.info("Drill: %s %s", type(drill), drill)
    logger.info("Screws_ids: %s %s ", type(screws_ids), screws_ids)
    logger.info("Plates_ids: %s %s ", type(plates_ids), plates_ids)
    logger.info("Images: %s %s ", type(images), images)
    result = await add_drill(session, drill, screws_ids, plates_ids, images)
    return result


@router.put("/update/{drill_id}", response_model=DrillSchema)
async def update_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_id: int,
    drill: DrillCreateSchema | str = Form(),
    screws_ids: list[str] = Form([]),
    plates_ids: list[str] = Form([]),
    images: list[UploadFile] = File([]),
) -> DrillSchema:

    logger.info("Update tool: %s %s %s", type(drill_id), drill_id, drill)

    result = await update_drill_in_db(session, drill_id, drill, screws_ids, plates_ids, images)
    return result


# Удаление сверла
@router.delete("/delete/{drill_id}", response_model=DrillSchema)
async def delete_drill(
    drill_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillSchema:
    result = await delete_drill_from_bd(session, drill_id)
    return result
