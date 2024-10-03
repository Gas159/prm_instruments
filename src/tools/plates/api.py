import logging
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import db_helper
from tools.plates.cruds import (
    add_plate,
    update_plate_in_db,
    delete_plate_from_db,
)
from tools.plates.models import PlateModel
from tools.plates.schemas import (
    PlateSchema,
    PlateCreateSchema,
    PlateUpdateSchema,
)

router = APIRouter()

logger = logging.getLogger(__name__)


# Get ONE
@router.get("/plate/{plate_id}", response_model=PlateSchema)
async def get_one_plate(
    plate_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> PlateModel:
    query = (
        select(PlateModel)
        .options(selectinload(PlateModel.drills))
        .where(PlateModel.id == plate_id)
    )
    result = await session.execute(query)
    plate = result.scalars().first()
    logger.info("Get plate: %s", plate)
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    return plate


# Get ALL
@router.get("/plates", response_model=List[PlateSchema])
async def get_all_plates(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> List[PlateModel]:
    query = select(PlateModel).options(selectinload(PlateModel.drills))
    result = await session.execute(query.order_by(PlateModel.id.desc()))
    plates = result.scalars().all()
    return list(plates)


@router.post("/plate/create", response_model=PlateSchema)
async def create_plate(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    plate: Annotated[PlateCreateSchema, Depends()],
    images: UploadFile = None,
) -> PlateSchema:
    logger.info("Images: %s", images)

    result = await add_plate(session, plate, images)
    return result


@router.put("/plate/update/{plate_id}", response_model=PlateSchema)
async def update_plate(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    plate_id: int,
    plate: PlateUpdateSchema,
) -> PlateModel:
    logger.info("Update plate: %s", plate)

    result = await update_plate_in_db(session, plate_id, plate)
    return result


@router.delete("/plate/delete/{plate_id}", response_model=PlateSchema)
async def delete_plate(
    plate_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> PlateSchema:
    result = await delete_plate_from_db(session, plate_id)
    return result
