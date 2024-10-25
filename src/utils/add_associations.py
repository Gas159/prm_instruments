import logging
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)


async def remove_associations(db: AsyncSession, association_table, drill_id):
    # Удаляем все ассоциации для сверла
    delete_stmt = delete(association_table).where(association_table.c.drill_id == drill_id)
    await db.execute(delete_stmt)
    await db.commit()


# Вспомогательная функция для добавления ассоциаций
async def add_associations(db: AsyncSession, association_table, drill_id, ids_list, id_field):
    try:
        ids = list(int(i) for i in ids_list[0].split(",") if i.strip().isdigit())  # reform ['1, 2, 3'] to [1, 2, 3]
        entries = [{"drill_id": drill_id, id_field: id_value} for id_value in ids]

        insert_stmt = insert(association_table).values(entries)
        logger.info("insert_stmt: %s %s", type(insert_stmt), insert_stmt)
        upsert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["drill_id", id_field])

        await db.execute(upsert_stmt)
        await db.commit()

        # Через проверку елементов
        # existing_associations = await db.execute(
        #     select(association_table)
        #     .where(association_table.c.drill_id == drill_id)
        #     .where(association_table.c[id_field].in_(ids))
        # )
        # logger.info("existing_associations: %s %s", type(existing_associations), existing_associations)
        #
        # existing_ids = set(row[1] for row in existing_associations.fetchall())
        # logger.info("existing_ids: %s %s", type(existing_ids), existing_ids)
        # new_ids = [id_value for id_value in ids if id_value not in existing_ids]
        #
        # if new_ids:
        #     entries = [{"drill_id": drill_id, id_field: id_value} for id_value in new_ids]
        #     await db.execute(insert(association_table).values(entries))
        # else:
        #     logger.info("No new associations to add")

    except Exception as e:
        await db.rollback()
        logger.error("Failed to add screws: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to add screws. {str(e)}")
