# main.py
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from fastapi import FastAPI, Depends, Request, Form, APIRouter, Query, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Annotated

from database import db_helper
from osnastka.models import ToolModel
from osnastka.schemas import STool, SToolBase, SToolCreate, SDeleteTool, SToolUpdate
from osnastka.cruds import (
    get_tools,
    add_tool,
    update_tool_in_db,
    delete_tool,
    get_all_diameters,
)
from starlette.responses import HTMLResponse, JSONResponse

router = APIRouter()
import logging

templates = Jinja2Templates(directory="templates")
# Настройка логгирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

loger = logging.getLogger(__name__)


# Получение всех свёрл
@router.get("/", response_class=HTMLResponse)
async def read_tools(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    sort_by: str = Query(
        "id",
        regex="^(id|name|diameter|length|deep_of_drill|plate|screws|key|company|is_broken)$",
    ),
    order: str = Query("asc", regex="^(asc|desc)$"),
    search: str | None = Query(""),
    diameter: List[float] = Query(None),  # Получение списка выбранных диаметров
) -> HTMLResponse:
    search = search.strip()
    tools = await get_tools(
        session, sort_by=sort_by, order=order, search=search, diameters=diameter
    )
    # Получаем список всех возможных диаметров для отображения в фильтре
    all_diameters = await get_all_diameters(session)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tools": tools,
            "sort_by": sort_by,
            "order": order,
            "search": search,
            "diameters": all_diameters,
            "selected_diameters": diameter or [],  # Отмечаем выбранные диаметры
        },
    )


# Создание сверла
@router.get("/create/", response_class=HTMLResponse)
async def create_tool_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@router.post("/create/")
async def create_tool(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    tool: SToolCreate,
):
    loger.info("Create tool: %s", tool)

    await add_tool(session, tool)
    return RedirectResponse("/", status_code=303)


# Обновление сверла
@router.get("/update/{tool_id}", response_class=HTMLResponse)
async def update_tool_view(
    request: Request,
    tool_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        stmt = select(ToolModel).where(ToolModel.id == tool_id)
        result = await session.execute(stmt)
        tool = result.scalars().first()

        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")

        return templates.TemplateResponse(
            "update.html", {"request": request, "tool": tool}
        )

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Tool not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{tool_id}")
async def update_tool(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    tool_id: int,
    tool: SToolUpdate,
):
    loger.info("Update tool: %s", tool)

    await update_tool_in_db(session, tool_id, tool)
    return RedirectResponse("/", status_code=303)


# Обновление статуса состояния инструмента
@router.post("/update_broken_status/{tool_id}")
async def update_tool_status(
    tool_id: int,
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):

    data = await request.json()
    is_broken = data.get("is_broken")

    # Получаем инструмент по ID
    tool = await session.get(ToolModel, tool_id)
    if not tool:
        return JSONResponse(status_code=404, content={"message": "Tool not found"})

    # Обновляем статус
    tool.is_broken = is_broken
    await session.commit()
    loger.info("Tool status updated successfully")
    return {"message": "Tool status updated successfully"}


# Удаление сверла
@router.post("/delete/{tool_id}")
async def delete_tool_view(
    tool_id: int, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    await delete_tool(session, tool_id)
    return RedirectResponse(url="/", status_code=303)
