import logging
from typing import List, Annotated

from fastapi import Depends, Request, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import db_helper
from tools.drills.models import DrillModel
from tools.drills.schemas import DrillSchema, DrillCreateSchema
from tools.drills.cruds import get_tools, add_drill, delete_tool, update_tool_in_db

router = APIRouter()


loger = logging.getLogger(__name__)


# Get ONE
@router.get("/{tool_id}", response_model=DrillSchema)
async def get_one(
    tool_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DrillModel:

    query = select(DrillModel).where(DrillModel.id == tool_id)
    result = await session.execute(query)
    tool = result.scalars().first()
    loger.info("Get tool: %s", tool)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


# Get ALL
@router.get("", response_model=List[DrillSchema])
async def get_all(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    #     sort_by: str = Query(
    #         "id",
    #         regex="^(id|name|diameter|length|deep_of_drill|plate|screws|key|company|is_broken)$",
    #     ),
    #     order: str = Query("asc", regex="^(asc|desc)$"),
    #     search: str | None = Query(""),
    #     diameter: List[float | None] = Query(None),  # Получение списка выбранных диаметров
) -> List[DrillModel]:
    #     search = search.strip()
    #     tools = await get_tools(
    #         session, sort_by=sort_by, order=order, search=search, diameters=diameter
    #     )
    #     # Получаем список всех возможных диаметров для отображения в фильтре
    #     all_diameters = await get_all_diameters(session)
    # return templates.TemplateResponse(
    #     "index.html",
    #     {
    #         "request": request,
    #         # "tools": tools,
    #         # "sort_by": sort_by,
    #         # "order": order,
    #         # "search": search,
    #         # "diameters": all_diameters,
    #         # "selected_diameters": diameter or [],  # Отмечаем выбранные диаметры
    #     },
    # )

    # Создание сверла
    query = select(DrillModel)
    result = await session.execute(query)
    drills = result.scalars().all()
    # Преобразование SQLAlchemy моделей в Pydantic
    return list(drills)


# @router.get("/create/", response_class=HTMLResponse)
# async def create_tool_form(request: Request):
#     return templates.TemplateResponse("create.html", {"request": request})
#
# #
@router.post("/create/")
async def create_drill(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    drill: DrillCreateSchema,
):
    loger.info("Create tool: %s", drill)

    result = await add_drill(session, drill)
    return result


#
# # Обновление сверла
# @router.get("/update/{tool_id}", response_class=HTMLResponse)
# async def update_tool_view(
#     request: Request,
#     tool_id: int,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ):
#     try:
#         stmt = select(ToolModel).where(ToolModel.id == tool_id)
#         result = await session.execute(stmt)
#         tool = result.scalars().first()
#
#         if not tool:
#             raise HTTPException(status_code=404, detail="Tool not found")
#
#         return templates.TemplateResponse(
#             "update.html", {"request": request, "tool": tool}
#         )
#
#     except NoResultFound:
#         raise HTTPException(status_code=404, detail="Tool not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.put("/update/{tool_id}")
# async def update_tool(
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#     tool_id: int,
#     tool: SToolUpdate,
# ):
#     loger.info("Update tool: %s", tool)
#
#     await update_tool_in_db(session, tool_id, tool)
#     return RedirectResponse("/", status_code=303)
#
#
# # Обновление статуса состояния инструмента
# @router.post("/update_broken_status/{tool_id}")
# async def update_tool_status(
#     tool_id: int,
#     request: Request,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ):
#     loger.info("Update tool status: %s", tool_id)
#     data = await request.json()
#     is_broken = data.get("is_broken")
#
#     # Получаем инструмент по ID
#     tool = await session.get(ToolModel, tool_id)
#     if not tool:
#         return JSONResponse(status_code=404, content={"message": "Tool not found"})
#
#     # Обновляем статус
#     tool.is_broken = is_broken
#     await session.commit()
#     loger.info("Tool status updated successfully")
#     return {"message": "Tool status updated successfully"}
#
#
# # Удаление сверла
# @router.delete("/delete/{tool_id}")
# async def delete_tool_view(
#     tool_id: int, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
# ):
#     await delete_tool(session, tool_id)
#     return RedirectResponse(url="/", status_code=303)
