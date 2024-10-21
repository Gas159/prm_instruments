# crud.py
import json
import logging
from sqlite3 import IntegrityError
from typing import List, Annotated

from fastapi import HTTPException, Form, File, UploadFile, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import upload_dir
from database import db_helper
from tools.archive.drills.models import DrillArchiveModel
from tools.drills.models import (
    DrillModel,
    drill_screw_association,
    drill_plate_association,
)
from tools.drills.schemas import (
    DrillCreateSchema,
    DrillSchema,
)
from utils.add_associations import add_associations
from utils.save_images import save_images

logger = logging.getLogger(__name__)

UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_drill(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill: DrillCreateSchema | str = Form(...),
    screws_ids: list[str] = Form([]),
    plates_ids: list[str] = Form([]),
    images: List[UploadFile] = File([]),
) -> DrillSchema:
    try:
        try:
            drill_data = json.loads(drill)
            logger.info("Parsed drill data: %s %s", type(drill_data), drill_data)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format" + str(e))

        new_drill = DrillModel(**drill_data)

        if images:
            drill_dir = upload_dir / "drills" / str(new_drill.id)
            drill_dir.mkdir(parents=True, exist_ok=True)
            new_drill.image_path = ", ".join(await save_images(images, drill_dir))

        db.add(new_drill)
        await db.commit()
        await db.refresh(new_drill)

        if screws_ids and screws_ids[0] != "":
            logger.info("Screws: %s IDs: %s", screws_ids, type(screws_ids))
            await add_associations(db, drill_screw_association, new_drill.id, screws_ids, "screw_id")

        if plates_ids and plates_ids[0] != "":
            logger.info("Plates: %s IDs: %s", plates_ids, type(plates_ids))
            await add_associations(db, drill_plate_association, new_drill.id, plates_ids, "plate_id")

        await db.commit()
        await db.refresh(new_drill, attribute_names=["screws", "plates"])
        drill_schema = DrillSchema.model_validate(new_drill)
        logger.info("Создано сверло: %s, добавлены винты: %s и пластины: %s", new_drill.id, screws_ids, plates_ids)

        return drill_schema

    except Exception as e:
        logger.error(f"Error from drill save: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error from drill save: ")


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


async def update_drill_in_db(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_id: int,
    drill: DrillCreateSchema | str = Form(),
    screws_ids: list[str] = Form([]),
    plates_ids: list[str] = Form([]),
    images: List[UploadFile] = File([]),
) -> DrillSchema:

    db_drill = await db.get(DrillModel, drill_id)
    logger.info("db_drill: %s %s", type(db_drill), db_drill)

    if db_drill is None:
        raise HTTPException(status_code=404, detail="drills not found")

    try:
        drill_data = json.loads(drill)
        logger.info("Parsed drill data: %s %s", type(drill_data), drill_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format" + str(e))

    try:
        for key, value in drill_data.items():
            logger.info("drills updated: %s %s ", key, value)

            if value is not None:
                setattr(db_drill, key, value)

        if screws_ids and screws_ids[0] != "":
            logger.info("Screws: %s IDs: %s", screws_ids, type(screws_ids))
            await add_associations(db, drill_screw_association, db_drill.id, screws_ids, "screw_id")

        if plates_ids and plates_ids[0] != "":
            logger.info("Plates: %s IDs: %s", plates_ids, type(plates_ids))
            await add_associations(db, drill_plate_association, db_drill.id, plates_ids, "plate_id")

        logger.info("Images: %s", images)

        if images:
            drill_dir = upload_dir / "drills" / str(db_drill.id)
            drill_dir.mkdir(parents=True, exist_ok=True)
            db_drill.image_path = ", ".join(await save_images(images, drill_dir))

        await db.commit()
        # await db.refresh(db_drill, attribute_names=["screws", "plates"])
        await db.refresh(db_drill)
        logger.info("Создано сверло: %s, добавлены винты: %s и пластины: %s", db_drill.id, screws_ids, plates_ids)
        logger.info("Update drills: %s", drill)
        return DrillSchema.model_validate(db_drill)
        # drill_dict = db_drill.__dict__
        # logger.info("Drill dict: %s", drill_dict)
        # return DrillSchema.model_validate(drill_dict)

    except IntegrityError:
        await db.rollback()
        raise Exception("Failed to upd drills: Integrity Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Какая то херня: " + str(e))


async def delete_drill_from_bd(db: AsyncSession, drill_id: int):

    query = select(DrillModel).where(DrillModel.id == drill_id)
    result = await db.execute(query)
    db_drill = result.scalar_one_or_none()

    if db_drill is None:
        raise HTTPException(status_code=404, detail="Drill not found")

    logger.info("Delete drills: %s %s", db_drill, db_drill.__dict__.items())

    try:
        drill_data = {key: value for key, value in db_drill.__dict__.items() if not key.startswith("_")}
        drill_archive = DrillArchiveModel(**drill_data)
        db.add(drill_archive)
        await db.delete(db_drill)
        await db.commit()

        logger.info("Drill archived and deleted: %s", drill_id)

    except Exception as e:
        await db.rollback()
        logger.error("Failed to archive and delete drills: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to archive and delete drills.g")

    return db_drill
