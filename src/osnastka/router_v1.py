# main.py

from fastapi import FastAPI, Depends, Request, Form, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Annotated

from database import db_helper
from osnastka.schemas import STool, SToolBase, SToolCreate, SDeleteTool, SToolUpdate
from osnastka.cruds import get_tools, add_tool, update_tool, delete_tool
from starlette.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_tools(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    sort_by: str = Query('id', regex='^(id|name|diameter|lenght|deep_of_drill)$'),
    order: str = Query('asc', regex='^(asc|desc)$'),
    search: Optional[str] = Query('')
):
    tools = await get_tools(session, sort_by=sort_by, order=order, search=search)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tools": tools,
        "sort_by": sort_by,
        "order": order,
        "search": search
    })


@router.get("/create/", response_class=HTMLResponse)
async def create_tool_form(request: Request):
	return templates.TemplateResponse("create.html", {"request": request})


@router.post("/create/")
async def create_tool(
		session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
		tool: SToolCreate,
):
	await add_tool(session, tool)
	return RedirectResponse("/", status_code=303)

# @router.post("/create/")
# async def create_tool_view(
# 		session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# 		tool_create: Annotated[SToolCreate, Depends()]):
# 	# tool = SToolCreate(**tool_create.dict())
# 	await create_tool(session, tool_create)
# 	return RedirectResponse(url="/", status_code=303)

#
#
# @app.post("/update/{tool_id}")
# async def update_tool_view(tool_id: int, name: str = Form(...),
# description: str = Form(...), category: str = Form(...),
#                            db: AsyncSession = Depends(get_db)):
# 	tool = ToolUpdate(name=name, description=description, category=category)
# 	await update_tool(db, tool_id, tool)
# 	return RedirectResponse(url="/", status_code=303)
#
#
# @app.post("/delete/{tool_id}")
# async def delete_tool_view(tool_id: int, db: AsyncSession = Depends(get_db)):
# 	await delete_tool(db, tool_id)
# 	return RedirectResponse(url="/", status_code=303)
