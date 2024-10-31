import json
import logging
import shutil
from sqlite3 import IntegrityError
from typing import List

from fastapi import HTTPException, UploadFile, Form, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import upload_dir
from tools.screws.models import ScrewModel
from tools.screws.schemas import ScrewCreateSchema, ScrewUpdateSchema, ScrewSchema
from utils.save_images import save_images

logger = logging.getLogger(__name__)

# Директория для загрузки изображений
UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_screw(
    db: AsyncSession,
    screw: ScrewCreateSchema | str = Form(...),
    images: list[UploadFile] = File([]),
) -> ScrewSchema:
    try:
        screw_data = json.loads(screw)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="invalid JSON format" + str(e))

    screw = ScrewModel(**screw_data)
    db.add(screw)
    await db.commit()
    await db.refresh(screw)

    if images:
        screw_dir = upload_dir / "screws" / str(screw.id)
        screw_dir.mkdir(parents=True, exist_ok=True)
        screw.image_path = ", ".join(await save_images(images, screw_dir))

    try:
        await db.commit()
        await db.refresh(screw)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to add screw: Integrity Error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    return ScrewSchema.model_validate(screw)


async def update_screw_in_db(
    db: AsyncSession,
    screw_id: int,
    screw: ScrewUpdateSchema | str = Form(),
    images: list[UploadFile] = File([]),
) -> ScrewSchema:
    logger.debug("Update screw: %s", screw_id)
    db_screw = await db.get(ScrewModel, screw_id)

    try:
        screw_data = json.loads(screw)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="invalid JSON format" + str(e))

    try:
        if db_screw is None:
            raise HTTPException(status_code=404, detail="Screw not found")

        # Применяем обновления только к тем полям, которые были установлены
        for key, value in screw_data.items():
            logger.info("Screw updated: %s %s ", key, value)

            if value is not None:
                setattr(db_screw, key, value)
        if images:
            screw_dir = upload_dir / "screws" / str(db_screw.id)
            screw_dir.mkdir(parents=True, exist_ok=True)
            db_screw.image_path = ", ".join(await save_images(images, screw_dir))

        logger.info("Update screw: %s", screw)

        await db.commit()
        await db.refresh(db_screw)
        return ScrewSchema.model_validate(db_screw)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update screw: Integrity Error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_screw_from_db(db: AsyncSession, screw_id: int):  # Изменено на delete_screw_from_db
    query = select(ScrewModel).where(ScrewModel.id == screw_id)
    result = await db.execute(query)
    db_screw = result.scalar_one_or_none()

    if db_screw is None:
        raise HTTPException(status_code=404, detail="Screw not found")

    logger.info("Delete screw: %s %s", db_screw, db_screw.__dict__.items())

    try:

        await db.delete(db_screw)
        await db.commit()

        logger.info("Screw archived and deleted: %s", screw_id)

    except Exception as e:
        await db.rollback()
        logger.error("Failed to archive and delete screw: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to archive and delete screw.")

    return db_screw  # Возвращаем удаленный объект
