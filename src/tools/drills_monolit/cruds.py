# crud.py
import json
import logging

from typing import List, Annotated

from fastapi import HTTPException, Form, File, UploadFile, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config import upload_dir
from database import db_helper


from tools.drills_monolit.models import DrillMonolitModel
from tools.drills_monolit.schemas import DrillMonolitCreateSchema, DrillMonolitSchema, DrillMonolitUpdateSchema
from utils.save_images import save_images

logger = logging.getLogger(__name__)

UPLOAD_DIR = upload_dir
UPLOAD_DIR.mkdir(exist_ok=True)


async def add_drill_monolit(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_monolit: DrillMonolitCreateSchema | str = Form(...),
    images: List[UploadFile] = File([]),
) -> DrillMonolitSchema:
    logger.debug("Add drill: %s, \n  images: %s", drill_monolit, images)
    try:
        try:
            drill_data = json.loads(drill_monolit)
            logger.info("Parsed drill data: %s %s", type(drill_data), drill_data)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format" + str(e))

        new_drill = DrillMonolitModel(**drill_data)

        db.add(new_drill)
        await db.commit()
        await db.refresh(new_drill)
        logger.info("Created drill: %s", new_drill)

        if images:
            drill_dir = upload_dir / "drills" / str(new_drill.id)
            drill_dir.mkdir(parents=True, exist_ok=True)
            new_drill.image_path = ", ".join(await save_images(images, drill_dir))

        await db.commit()
        await db.refresh(new_drill)
        # await db.refresh(new_drill, attribute_names=["screws", "plates"])
        drill_schema = DrillMonolitSchema.model_validate(new_drill)
        logger.info(
            "Создано сверло: %s",
            new_drill.id,
        )
        return drill_schema

    except Exception as e:
        logger.info(f"Error from drill save: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error from drill save: {str(e)}")


async def update_drill_monolit_in_db(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill_id: int,
    drill: DrillMonolitUpdateSchema | str = Form(),
    images: List[UploadFile] = File([]),
) -> DrillMonolitSchema:

    db_drill = await db.get(DrillMonolitModel, drill_id)
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

        logger.info("Images: %s", images)

        if images:
            drill_dir = upload_dir / "drills" / str(db_drill.id)
            drill_dir.mkdir(parents=True, exist_ok=True)
            db_drill.image_path = ", ".join(await save_images(images, drill_dir))

        await db.commit()
        await db.refresh(db_drill)
        logger.info("Создано сверло: %s", db_drill.id)
        logger.info("Update drills: %s", drill)
        return DrillMonolitSchema.model_validate(db_drill)

    except IntegrityError:
        await db.rollback()
        raise Exception("Failed to upd drills: Integrity Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Какая то херня: " + str(e))


async def delete_drill_monolit_from_bd(db: AsyncSession, drill_id: int):

    query = select(DrillMonolitModel).where(DrillMonolitModel.id == drill_id)
    result = await db.execute(query)
    db_drill = result.unique().scalar_one_or_none()

    if db_drill is None:
        raise HTTPException(status_code=404, detail="Drill not found")

    logger.info("Delete drills: %s %s", db_drill, db_drill.__dict__.items())

    try:
        # Исключаем связь с винтами и пластинами при архивировании сверла
        # drill_data = {
        #     key: value
        #     for key, value in db_drill.__dict__.items()
        #     if not key.startswith("_") and key not in ["screws", "plates"]
        # }
        # drill_data = {key: value for key, value in db_drill.__dict__.items() if not key.startswith("_")}
        # drill_archive = DrillArchiveModel(**drill_data)
        # db.add(drill_archive)
        await db.delete(db_drill)
        await db.commit()

        logger.info("Drill archived and deleted: %s", drill_id)

    except Exception as e:
        await db.rollback()
        logger.error("Failed to archive and delete drills: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to archive and delete drills.g")

    return db_drill
