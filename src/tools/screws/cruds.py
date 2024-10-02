import logging
import shutil
from pathlib import Path
from sqlite3 import IntegrityError
from typing import List, Annotated

from fastapi import HTTPException, UploadFile
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from config import upload_dir
from tools.screws.models import ScrewModel
from tools.screws.schemas import ScrewCreateSchema, ScrewUpdateSchema

logger = logging.getLogger(__name__)

# Директория для загрузки изображений
UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_screw(  # Изменено на add_screw
    db: AsyncSession,
    screw: ScrewCreateSchema,  # Изменено на ScrewCreateSchema
    images: List[UploadFile] | None = None,  # Изменено на List[UploadFile]
):
    screw = ScrewModel(**screw.model_dump())  # Создание экземпляра ScrewModel
    db.add(screw)

    logger.info("Add screw: %s", screw)

    try:
        await db.commit()
        await db.refresh(screw)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Failed to add screw: Integrity Error"
        )
    except Exception as e:
        await db.rollback()  # Откат для всех других исключений
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    logger.info("Images: %s", images)

    # if not isinstance(images, list):
    #     images = []  # Если файлы не переданы, инициализируем пустой список

    # Проверка и сохранение изображения, если оно есть
    if images:
        screw_dir = upload_dir / "screws" / str(screw.id)  # Заменено на screws
        screw_dir.mkdir(parents=True, exist_ok=True)

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
            file_path = screw_dir / file_name

            # Сохранение файла на диск
            try:
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)

                # Сохранение пути к изображению в модели винта
                image_paths.append(str(file_path))

            except Exception as e:
                logger.error(f"Error saving image: {str(e)}")
                await db.rollback()
                raise HTTPException(status_code=500, detail="Error saving image.")

        # Присвоим список путей изображений объекту модели винта
        logger.debug("image_paths: %s", image_paths)
        screw.image_path = ", ".join(image_paths)
        logger.debug("Screw.image_path: %s", screw.image_path)

        # Повторный коммит для сохранения пути к файлу
        await db.commit()
        await db.refresh(screw)

    return screw  # Возвращаем экземпляр ScrewModel


async def update_screw_in_db(
    db: AsyncSession, screw_id: int, screw: ScrewUpdateSchema
):  # Изменено на update_screw_in_db
    db_screw = await db.get(ScrewModel, screw_id)  # Получение существующей записи

    try:
        if db_screw is None:
            raise HTTPException(status_code=404, detail="Screw not found")

        # Применяем обновления только к тем полям, которые были установлены
        for key, value in screw.model_dump(exclude_unset=True).items():
            logger.info("Screw updated: %s %s ", key, value)

            if value is not None:  # Пропускаем поля с None
                setattr(db_screw, key, value)

        logger.info("Update screw: %s", screw)

        await db.commit()
        await db.refresh(db_screw)
        return db_screw

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Failed to update screw: Integrity Error"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_screw_from_db(
    db: AsyncSession, screw_id: int
):  # Изменено на delete_screw_from_db
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
        raise HTTPException(
            status_code=500, detail="Failed to archive and delete screw."
        )

    return db_screw  # Возвращаем удаленный объект
