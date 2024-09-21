# crud.py
from fastapi import HTTPException
from sqlite3 import IntegrityError
from typing import Optional, List

from sqlalchemy.future import select
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from osnastka.models import ToolModel
from osnastka.schemas import SToolCreate, SToolUpdate
from fastapi.responses import RedirectResponse


async def get_tools(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    sort_by: str = "id",
    order: str = "asc",
    search: str = None,
    diameters: Optional[List[float]] = None,
):
    query = select(ToolModel)
    if search:
        query = query.where(ToolModel.name.ilike(f"%{search}%"))

    if diameters:
        query = query.where(ToolModel.diameter.in_(diameters))

    if order == "asc":
        query = query.order_by(asc(getattr(ToolModel, sort_by)))
    else:
        query = query.order_by(desc(getattr(ToolModel, sort_by)))
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_all_diameters(session: AsyncSession):
    query = select(ToolModel.diameter).distinct()
    result = await session.execute(query)
    return sorted([row[0] for row in result.fetchall()])


async def add_tool(db: AsyncSession, tool: SToolCreate):
    db_tool = ToolModel(**tool.model_dump())
    db.add(db_tool)
    try:
        await db.commit()
        await db.refresh(db_tool)

    except IntegrityError:
        await db.rollback()
        raise Exception("Failed to add tool: Integrity Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_tool_in_db(db: AsyncSession, tool_id: int, tool: SToolUpdate):
    db_tool = await db.get(ToolModel, tool_id)

    try:

        if db_tool is None:
            raise HTTPException(status_code=404, detail="Tool not found")

        for key, value in tool.model_dump(exclude_unset=True).items():
            if value is None:
                continue
            setattr(db_tool, key, value)

        await db.commit()
        await db.refresh(db_tool)

    except IntegrityError:
        await db.rollback()
        raise Exception("Failed to add tool: Integrity Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_tool(db: AsyncSession, tool_id: int):
    db_tool = await db.get(ToolModel, tool_id)
    if db_tool is None:
        return None
    await db.delete(db_tool)
    await db.commit()


# return db_tool
