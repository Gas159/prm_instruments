# crud.py
import logging
import shutil
from sqlite3 import IntegrityError
from typing import List, Annotated

from fastapi import HTTPException, UploadFile, File, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import upload_dir
from tools.archive.drills.models import DrillArchiveModel
from tools.drills.models import DrillModel
from tools.drills.schemas import DrillCreateSchema, DrillUpdateSchema, DrillSchema
from tools.screws.models import ScrewModel

loger = logging.getLogger(__name__)

UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_drill(
    db: AsyncSession,
    drill: DrillCreateSchema,
    screws_ids,
    images,
    # images: Annotated[UploadFile, File(...)] = None,
    # screw_ids: List[int] | None = Form(...),  # Важно: список ID винтов
    # images: List[UploadFile] = File(None),  # Важно: загрузка файлов
    # images: List[UploadFile] | None = None,
    # images: List[UploadFile] | None = None,
    # images: Annotated[List[UploadFile], File([])] | None = None,
) -> DrillSchema:

    loger.info("Screws: %s IDs: %s", screws_ids, type(screws_ids))

    drill = DrillModel(**drill.model_dump())

    if screws_ids and None not in screws_ids and "" not in screws_ids:

        screws_ids = list(
            int(i)
            for i in screws_ids[0].split(",")
            if i.strip().isdigit() and int(i) != 0
        )
        loger.info("Screws ids: %s %s", screws_ids, type(screws_ids))
        screws_query = await db.execute(
            select(ScrewModel).where(ScrewModel.id.in_(screws_ids))
        )
        screws = screws_query.scalars().all()

        loger.info("lenScrews: %s, Len Idis: %s", len(screws), len(screws_ids))
        if len(screws) != len(screws_ids):
            raise HTTPException(status_code=400, detail="Some screws were not found.")
        drill.screws.extend(screws)

    loger.info("Screws: %s", screws_ids)
    loger.info("DrillScrews: %s", drill.screws)

    db.add(drill)

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

    #
    # if not isinstance(images, list):
    #     images = []  # Если файлы не переданы, инициализируем пустой список
    loger.info("Images: %s", images)

    # Проверка и сохранение изображения, если оно есть
    if images:
        drill_dir = upload_dir / "drills" / str(drill.id)
        drill_dir.mkdir(parents=True, exist_ok=True)

        image_paths = []
        if not isinstance(images, list):
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

    query = (
        select(DrillModel)
        .where(DrillModel.id == drill.id)
        .options(selectinload(DrillModel.screws))
    )
    result = await db.execute(query)
    drill = result.scalars().first()
    return drill


# Директория для загрузки изображений


UPLOAD_DIR = upload_dir

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


UPLOAD_DIR.mkdir(exist_ok=True)


async def update_drill_in_db(db: AsyncSession, drill_id: int, drill: DrillUpdateSchema):
    db_drill = await db.get(DrillModel, drill_id)

    try:

        if db_drill is None:
            raise HTTPException(status_code=404, detail="drills not found")

        # Применяем обновления только к тем полям, которые были установлены
        for key, value in drill.model_dump(exclude_unset=True).items():
            loger.info("drills updated: %s %s ", key, value)

            if value is not None:  # Пропускаем поля с None
                setattr(db_drill, key, value)

        loger.info("Update drills: %s", drill)

        await db.commit()
        await db.refresh(db_drill)
        return db_drill

    except IntegrityError:
        await db.rollback()
        raise Exception("Failed to add drills: Integrity Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_drill_from_bd(db: AsyncSession, drill_id: int):

    # db_drill = await db.get(DrillModel, drill_id)
    # query = select(DrillModel).where(DrillModel.id == tool_id)
    query = select(DrillModel).where(DrillModel.id == drill_id)
    result = await db.execute(query)
    db_drill = result.scalar_one_or_none()

    if db_drill is None:
        raise HTTPException(status_code=404, detail="Drill not found")

    loger.info("Delete drills: %s %s", db_drill, db_drill.__dict__.items())

    try:
        drill_data = {
            key: value
            for key, value in db_drill.__dict__.items()
            if not key.startswith("_")
        }
        drill_archive = DrillArchiveModel(**drill_data)
        db.add(drill_archive)
        await db.delete(db_drill)
        await db.commit()

        loger.info("Drill archived and deleted: %s", drill_id)

    except Exception as e:
        await db.rollback()
        loger.error("Failed to archive and delete drills: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to archive and delete drills.g"
        )

    return db_drill
