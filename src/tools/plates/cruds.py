import logging
import shutil
from pathlib import Path
from sqlite3 import IntegrityError
from typing import List, Annotated

from fastapi import HTTPException, UploadFile
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import upload_dir
from tools.plates.models import PlateModel
from tools.plates.schemas import PlateCreateSchema, PlateUpdateSchema

logger = logging.getLogger(__name__)

# Директория для загрузки изображений
UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_plate(
    db: AsyncSession,
    plate: PlateCreateSchema,
    images: List[UploadFile] | None = None,
):
    plate = PlateModel(**plate.model_dump())
    db.add(plate)

    logger.info("Add plate: %s", plate)

    try:
        await db.commit()
        await db.refresh(plate)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Failed to add plate: Integrity Error"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )

    logger.info("Images: %s", images)

    # Проверка и сохранение изображения, если оно есть
    if images:
        plate_dir = upload_dir / "plates" / str(plate.id)
        plate_dir.mkdir(parents=True, exist_ok=True)

        image_paths = []
        images = [images]

        for image in images:
            if image is None:
                continue
            if not image.content_type.startswith("image/"):
                raise HTTPException(
                    status_code=400, detail="Uploaded file is not an image."
                )

            # Генерация уникального имени файла
            file_ext = image.filename.split(".")[-1]
            file_first_name = image.filename.split(".")[0]
            file_name = f"{file_first_name}.{file_ext}"
            file_path = plate_dir / file_name

            # Сохранение файла на диск
            try:
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)

                # Сохранение пути к изображению в модели пластин
                image_paths.append(str(file_path))

            except Exception as e:
                logger.error(f"Error saving image: {str(e)}")
                await db.rollback()
                raise HTTPException(
                    status_code=500, detail="Error saving image."
                )

        # Присвоим список путей изображений объекту модели пластины
        logger.debug("image_paths: %s", image_paths)
        plate.image_path = ", ".join(image_paths)
        logger.debug("Plate.image_path: %s", plate.image_path)

        # Повторный коммит для сохранения пути к файлу
        await db.commit()
        await db.refresh(plate)
    query = (
        select(PlateModel)
        .where(PlateModel.id == plate.id)
        .options(selectinload(PlateModel.drills))
    )
    result = await db.execute(query)
    plate = result.scalars().first()
    return plate


async def update_plate_in_db(
    db: AsyncSession, plate_id: int, plate: PlateUpdateSchema
):  # Изменено на update_plate_in_db
    db_plate = await db.get(
        PlateModel, plate_id
    )  # Получение существующей записи

    try:
        if db_plate is None:
            raise HTTPException(status_code=404, detail="Plate not found")

        # Применяем обновления только к тем полям, которые были установлены
        for key, value in plate.model_dump(exclude_unset=True).items():
            logger.info("Plate updated: %s %s ", key, value)

            if value is not None:  # Пропускаем поля с None
                setattr(db_plate, key, value)

        logger.info("Update plate: %s", plate)

        await db.commit()
        await db.refresh(db_plate)
        return db_plate

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Failed to update plate: Integrity Error"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_plate_from_db(
    db: AsyncSession, plate_id: int
):  # Изменено на delete_plate_from_db
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
        raise HTTPException(
            status_code=500, detail="Failed to archive and delete plate."
        )

    return db_plate  # Возвращаем удаленный объект
