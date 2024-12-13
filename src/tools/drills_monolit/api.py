import logging
from loggind_config import setup_logging
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, Query, UploadFile, File, Form
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper


from tools.drills_monolit.cruds import add_drill_monolit, update_drill_monolit_in_db, delete_drill_monolit_from_bd
from tools.drills_monolit.models import DrillMonolitModel
from tools.drills_monolit.schemas import DrillMonolitSchema, DrillMonolitCreateSchema, DrillMonolitUpdateSchema

# setup_logging()
logger = logging.getLogger("my_logger")
logger.propagate = False

router = APIRouter(tags=["Drills_monolit"], prefix="/drills_monolit")


# Get ONE
@router.get("/{tool_id}", response_model=DrillMonolitSchema)
async def get_one(
    tool_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillMonolitSchema:

    query = select(DrillMonolitModel).where(DrillMonolitModel.id == tool_id)
    result = await session.execute(query)
    tool = result.scalars().first()
    logger.info("Get tool: %s", tool)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return DrillMonolitSchema.model_validate(tool)


# Get ALL


@router.get(
    "s",
    response_model=List[DrillMonolitSchema],
    # dependencies=[Depends(role_checker("admin"))],
    # dependencies=[Depends(lambda: role_checker("admin"))],
)
async def get_all(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    broken: bool | None = Query(False),
    diameter: List[float] | None = Query(None),  # Получение списка выбранных диаметров
) -> List[DrillMonolitSchema]:

    logger.debug("Get tools: %s", broken)

    query = select(DrillMonolitModel)
    filters = []
    if broken is not None:
        logger.debug("Check broken: %s", broken)
        filters.append(DrillMonolitModel.is_broken == broken)

    if diameter is not None:
        logger.debug("Check diameter: %s", diameter)
        filters.append(DrillMonolitModel.diameter.in_(diameter))

    # Применение фильтров к запросу
    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query.order_by(DrillMonolitModel.id.desc()))
    drills = result.scalars().all()
    validated_drills = [DrillMonolitSchema.model_validate(drill) for drill in drills]
    return validated_drills


# Create Drill


@router.post("/create", response_model=DrillMonolitSchema)
async def create_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_monolit: DrillMonolitCreateSchema | str = Form(...),
    images: list[UploadFile] = File([]),
) -> DrillMonolitSchema:
    logger.debug("Add drill: %s, \n  images: %s", drill_monolit, images)
    result = await add_drill_monolit(session, drill_monolit, images)
    return result


@router.put("/update/{drill_id}", response_model=DrillMonolitSchema)
async def update_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_id: int,
    drill: DrillMonolitUpdateSchema | str = Form(),
    images: list[UploadFile] = File([]),
) -> DrillMonolitSchema:

    logger.info("Update tool: %s %s %s", type(drill_id), drill_id, drill)

    result = await update_drill_monolit_in_db(session, drill_id, drill, images)
    return result


# Удаление сверла
@router.delete("/delete/{drill_id}", response_model=DrillMonolitSchema)
async def delete_drill(
    drill_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillMonolitSchema:
    result = await delete_drill_monolit_from_bd(session, drill_id)
    return result
