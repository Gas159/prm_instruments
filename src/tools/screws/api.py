import logging
from typing import List, Annotated, Union, Optional

from fastapi import Depends, APIRouter, HTTPException, Query, UploadFile, File
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import db_helper
from tools.screws.models import ScrewModel
from tools.screws.schemas import (
    ScrewSchema,
    ScrewCreateSchema,
    ScrewUpdateSchema,
)
from tools.screws.cruds import (
    add_screw,
    update_screw_in_db,
    delete_screw_from_db,
)

router = APIRouter()

logger = logging.getLogger(__name__)


# Get ONE
@router.get("/screw/{screw_id}", response_model=ScrewSchema)
async def get_one_screw(
    screw_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ScrewModel:
    query = (
        select(ScrewModel)
        .options(selectinload(ScrewModel.drills))
        .where(ScrewModel.id == screw_id)
    )
    result = await session.execute(query)
    screw = result.scalars().first()
    logger.info("Get screw: %s", screw)
    if not screw:
        raise HTTPException(status_code=404, detail="Screw not found")
    return screw


# Get ALL
@router.get("/screws", response_model=List[ScrewSchema])
async def get_all_crews(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    # broken: bool | None = Query(False),
    # diameter: List[float] | None = Query(None),
) -> List[ScrewModel]:
    # logger.debug("Get screws: %s", broken)

    query = select(ScrewModel).options(
        selectinload(ScrewModel.drills)
    )  # Заменено на ScrewModel.drills

    # filters = []
    # if broken is not None:
    #     logger.debug("Check broken: %s", broken)
    #     filters.append(ScrewModel.is_broken == broken)
    #
    # if diameter is not None:
    #     logger.debug("Check diameter: %s", diameter)
    #     filters.append(ScrewModel.diameter.in_(diameter))

    # if filters:
    #     query = query.where(and_(*filters))

    result = await session.execute(query.order_by(ScrewModel.id.desc()))
    screws = result.scalars().all()
    return list(screws)


@router.post("/screw/create")
async def create_screw(  # Изменено на create_screw
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    screw: Annotated[ScrewCreateSchema, Depends()],  # Изменено на ScrewCreateSchema
    images: UploadFile = None,
) -> ScrewSchema:  # Изменено на ScrewSchema
    logger.info("Images: %s", images)

    result = await add_screw(session, screw, images)  # Изменено на add_screw
    return result


@router.put(
    "/screw/update/{screw_id}", response_model=ScrewSchema
)  # Изменено на screw_id
async def update_screw(  # Изменено на update_screw
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    screw_id: int,  # Изменено на screw_id
    screw: ScrewUpdateSchema,  # Изменено на ScrewUpdateSchema
) -> ScrewModel:
    logger.info("Update screw: %s", screw)

    result = await update_screw_in_db(
        session, screw_id, screw
    )  # Изменено на update_screw_in_db
    return result


# Удаление винта
@router.delete(
    "/screw/delete/{screw_id}", response_model=ScrewSchema
)  # Изменено на screw_id
async def delete_screw(  # Изменено на delete_screw
    screw_id: int,  # Изменено на screw_id
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ScrewSchema:
    result = await delete_screw_from_db(
        session, screw_id
    )  # Изменено на delete_screw_from_db
    return result
