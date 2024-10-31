import json
import logging
import shutil
from json import JSONDecodeError
from pathlib import Path
from sqlite3 import IntegrityError
from typing import List, Annotated

from fastapi import HTTPException, UploadFile, Depends, Form, File
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import upload_dir
from database import db_helper
from tools.plates.models import PlateModel
from tools.plates.schemas import PlateCreateSchema, PlateUpdateSchema, PlateSchema
from utils.save_images import save_images

logger = logging.getLogger(__name__)

# Директория для загрузки изображений
UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_plate(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    plate: PlateCreateSchema | str = Form(...),
    images: list[UploadFile] = File([]),
) -> PlateSchema:

    try:
        plate_data = json.loads(plate)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="invalid JSON format" + str(e))

    new_plate = PlateModel(**plate_data)

    db.add(new_plate)
    await db.commit()
    await db.refresh(new_plate)

    try:
        if images:
            plate_dir = upload_dir / "plates" / str(new_plate.id)
            plate_dir.mkdir(parents=True, exist_ok=True)
            new_plate.image_path = ", ".join(await save_images(images, plate_dir))

        db.add(new_plate)
        await db.commit()
        await db.refresh(new_plate)
        return PlateSchema.model_validate(new_plate)
    except Exception as e:
        logger.error(f"Error from plate save: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error from plate save: ")


async def update_plate_in_db(
    db: AsyncSession,
    plate_id: int,
    plate: PlateUpdateSchema | str = Form(),
    images: list[UploadFile] = File([]),
) -> PlateSchema:
    db_plate = await db.get(PlateModel, plate_id)

    try:
        if db_plate is None:
            raise HTTPException(status_code=404, detail="Plate not found")

        try:
            plate_data = json.loads(plate)
        except JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="invalid JSON format" + str(e))

        for key, value in plate_data.items():
            logger.info("Plate updated: %s %s ", key, value)

            if value is not None:
                setattr(db_plate, key, value)
        if images:
            plate_dir = upload_dir / "plates" / str(db_plate.id)
            plate_dir.mkdir(parents=True, exist_ok=True)
            db_plate.image_path = ", ".join(await save_images(images, plate_dir))

        logger.info("Update plate: %s", plate)

        await db.commit()
        await db.refresh(db_plate)
        return PlateSchema.model_validate(db_plate)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update plate: Integrity Error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_plate_from_db(db: AsyncSession, plate_id: int):
    query = select(PlateModel).where(PlateModel.id == plate_id)
    result = await db.execute(query)
    db_plate = result.scalar_one_or_none()

    if db_plate is None:
        raise HTTPException(status_code=404, detail="Plate not found")

    logger.info("Delete plate: %s %s", db_plate, db_plate.__dict__.items())

    try:

        await db.delete(db_plate)
        await db.commit()

        logger.info("Plate archived and deleted: %s", plate_id)

    except Exception as e:
        await db.rollback()
        logger.error("Failed to archive and delete plate: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to archive and delete plate.")

    return db_plate
