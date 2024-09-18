# crud.py
from sqlite3 import IntegrityError

from sqlalchemy.future import select
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from osnastka.models import ToolModel
from osnastka.schemas import SToolCreate, SToolUpdate


async def get_tools(db: AsyncSession, skip: int = 0, limit: int = 10, sort_by: str = 'id', order: str = 'asc',
                    search: str = None):
	query = select(ToolModel)
	if search:
		query = query.filter(ToolModel.name.ilike(f"%{search}%"))
	if order == 'asc':
		query = query.order_by(asc(getattr(ToolModel, sort_by)))
	else:
		query = query.order_by(desc(getattr(ToolModel, sort_by)))
	result = await db.execute(query.offset(skip).limit(limit))
	return result.scalars().all()


async def add_tool(db: AsyncSession, tool: SToolCreate):
	db_tool = ToolModel(**tool.model_dump())
	db.add(db_tool)
	try:
		await db.commit()
		await db.refresh(db_tool)
	except IntegrityError:
		await db.rollback()
		raise Exception("Failed to add tool: Integrity Error")


async def update_tool(db: AsyncSession, tool_id: int, tool: SToolUpdate):
	db_tool = await db.get(ToolModel, tool_id)
	if db_tool is None:
		return None
	for key, value in tool.dict().items():
		setattr(db_tool, key, value)
	await db.commit()
	await db.refresh(db_tool)
	return db_tool


async def delete_tool(db: AsyncSession, tool_id: int):
	db_tool = await db.get(ToolModel, tool_id)
	if db_tool is None:
		return None
	await db.delete(db_tool)
	await db.commit()
	return db_tool
