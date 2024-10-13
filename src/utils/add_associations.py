import logging
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


# Вспомогательная функция для добавления ассоциаций
async def add_associations(db: AsyncSession, association_table, drill_id, ids_list, id_field):
    try:
        ids = list(int(i) for i in ids_list[0].split(",") if i.strip().isdigit())  # reform ['1, 2, 3'] to [1, 2, 3]
        entries = [{"drill_id": drill_id, id_field: id_value} for id_value in ids]
        await db.execute(insert(association_table).values(entries))

    except Exception as e:
        await db.rollback()
        logger.error("Failed to add screws: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to add screws. {str(e)}")
