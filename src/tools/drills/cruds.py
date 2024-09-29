# crud.py
import logging
from sqlite3 import IntegrityError

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from tools.drills.models import DrillModel
from tools.drills.schemas import DrillCreateSchema

loger = logging.getLogger(__name__)


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


async def add_drill(db: AsyncSession, drill: DrillCreateSchema):
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

    return drill


#
#
# async def update_tool_in_db(db: AsyncSession, tool_id: int, tool: SToolUpdate):
#     db_tool = await db.get(ToolModel, tool_id)
#
#     try:
#
#         if db_tool is None:
#             raise HTTPException(status_code=404, detail="Tool not found")
#
#         # Применяем обновления только к тем полям, которые были установлены
#         for key, value in tool.model_dump(exclude_unset=True).items():
#             loger.info("Tool updated: %s %s ", key, value)
#
#             if value is not None:  # Пропускаем поля с None
#                 setattr(db_tool, key, value)
#
#         loger.info("Update tool: %s", tool)
#
#         await db.commit()
#         await db.refresh(db_tool)
#
#     except IntegrityError:
#         await db.rollback()
#         raise Exception("Failed to add tool: Integrity Error")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# async def delete_tool(db: AsyncSession, tool_id: int):
#     db_tool = await db.get(ToolModel, tool_id)
#     if db_tool is None:
#         return None
#     await db.delete(db_tool)
#     await db.commit()
#
#
# # return db_tool
