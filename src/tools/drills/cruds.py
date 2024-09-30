# crud.py
import logging
import shutil
import uuid
from pathlib import Path
from sqlite3 import IntegrityError
from typing import List, Union, Annotated, Optional

from fastapi import HTTPException, UploadFile, File
from markdown_it.rules_inline import image
from sqlalchemy.ext.asyncio import AsyncSession

from tools.drills.models import DrillModel
from tools.drills.schemas import DrillCreateSchema, DrillUpdateSchema

loger = logging.getLogger(__name__)

# Директория для загрузки изображений
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

# async def get_tools(
#     db: AsyncSession,
#     skip: int = 0,
#     limit: int = 50,
#     sort_by: str = "id",
#     order: str = "asc",
#     search: str = None,
#     diameters: Optional[List[float | None]] = None,
# ):
#     query = select(ToolModel)
#     if search:
#         query = query.where(ToolModel.name.ilike(f"%{search}%"))
#
#     if diameters:
#         query = query.where(ToolModel.diameter.in_(diameters))
#
#     if order == "asc":
#         query = query.order_by(asc(getattr(ToolModel, sort_by)))
#     else:
#         query = query.order_by(desc(getattr(ToolModel, sort_by)))
#     result = await db.execute(query.offset(skip).limit(limit))
#     return result.scalars().all()
#
#
# async def get_all_diameters(session: AsyncSession):
#     query = select(ToolModel.diameter).distinct()
#     result = await session.execute(query)
#     return sorted([row[0] for row in result.fetchall()], key=lambda x: (x is None, x))
#
#
# # return sorted([row[0] for row in result.fetchall() ])


async def add_drill(
    db: AsyncSession,
    drill: DrillCreateSchema,
    images: List[UploadFile] = None,
    # images: UploadFile = None,
    # images: List[UploadFile] | None = None,
    # images: Annotated[List[UploadFile], File([])] | None = None,
):
    if not isinstance(images, list):
        images = []  # Если файлы не переданы, инициализируем пустой список

    drill = DrillModel(**drill.model_dump())
    db.add(drill)

    loger.info("Add tool: %s", drill)

    try:
        await db.commit()
        await db.refresh(drill)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Failed to add tool: Integrity Error"
        )
    except Exception as e:
        await db.rollback()  # Откат для всех других исключений
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    loger.info("Images: %s", images)
    if not images:
        images = []  # Если файлы не переданы, инициализируем пустой список
    # Проверка и сохранение изображения, если оно есть
    if images:
        # Создание директории для хранения изображений, уникальной для каждого сверла по его ID
        drill_dir = UPLOAD_DIR / "drills" / str(drill.id)
        drill_dir.mkdir(exist_ok=True)

        image_paths = []

        for image in images:
            if image is None:
                continue
            if not image.content_type.startswith("image/"):
                raise HTTPException(
                    status_code=400, detail="Uploaded file is not an image."
                )

            # Генерация уникального имени файла
            file_ext = image.filename.split(".")[-1]
            file_first_name = drill.name.split(".")[0]
            file_name = f"drill_{drill.id}_{file_first_name}.{file_ext}"
            file_path = drill_dir / file_name

            # Сохранение файла на диск
            try:
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)

                # Сохранение пути к изображению в модели сверла
                image_paths.append(str(file_path))

            except Exception as e:
                loger.error(f"Error saving image: {str(e)}")
                await db.rollback()
                raise HTTPException(status_code=500, detail="Error saving image.")

        # Присвоим список путей изображений объекту модели сверла
        loger.debug("image_paths: %s", image_paths)
        drill.image_path = ", ".join(image_paths)
        loger.debug("Drill.image_path: %s", drill.image_path)

        # Повторный коммит для сохранения пути к файлу
        await db.commit()
        await db.refresh(drill)
    # drill.image_path = ",".join(image_paths)
    # drill.image_path = "tests string"
    return drill


async def update_drill_in_db(db: AsyncSession, drill_id: int, drill: DrillUpdateSchema):
    db_drill = await db.get(DrillModel, drill_id)

    try:

        if db_drill is None:
            raise HTTPException(status_code=404, detail="drill not found")

        # Применяем обновления только к тем полям, которые были установлены
        for key, value in drill.model_dump(exclude_unset=True).items():
            loger.info("drill updated: %s %s ", key, value)

            if value is not None:  # Пропускаем поля с None
                setattr(db_drill, key, value)

        loger.info("Update drill: %s", drill)

        await db.commit()
        await db.refresh(db_drill)
        return db_drill

    except IntegrityError:
        await db.rollback()
        raise Exception("Failed to add drill: Integrity Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_drill_from_bd(db: AsyncSession, drill_id: int):
    db_drill = await db.get(DrillModel, drill_id)
    if db_drill is None:
        raise HTTPException(status_code=404, detail="Drill not found")
    await db.delete(db_drill)
    await db.commit()
    return db_drill
