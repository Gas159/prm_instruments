import logging

import aiohttp
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import selectinload, sessionmaker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import main_app as app  # замените на ваш файл, где определен app
from tools.drills.models import DrillModel  # замените на ваши модели
from tools.drills.schemas import DrillSchema  # замените на ваши схемы
from database import db_helper

# from database import get_db  # замените на вашу функцию получения сессии
from project_services.base import Base


logger = logging.getLogger(__name__)
TEST_DATABASE_URL = "postgresql+asyncpg://gas:123@localhost:5433/test"
engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False)



# @pytest.fixture(scope="module")
# async def test_db():
#     # Создаем сессию
#     async with AsyncSessionLocal() as session:
#         # Если необходимо, можно вставить начальные данные в базу данных здесь
#         yield session  # Возвращаем сессию для использования в тестах


# @pytest.fixture
# async def client(test_db):
#     async with AsyncClient(app=app, base_url="http://test") as test_client:
#         yield test_client  # Возвращаем клиент для использования в тестах

#
# client = TestClient(app)
# @pytest.fixture(scope="module")
# async def test_db():
#     async with AsyncSession() as session:
#         drill = DrillModel( name="Test Drill")
#         session.add(drill)
#         await session.commit()
#         await session.refresh(drill)
#         yield session  # Возвращает сессию для тестов
        # await session.run_sync(Base.metadata.drop_all)  # Очищает базу данных после тестов

# @pytest.mark.asyncio
# async def test_read_main(test_db):
#     query = select(DrillModel).options(selectinload(DrillModel.plates), selectinload(DrillModel.screws))
#     result = await session.execute(query)
#     tool = result.scalars().first()
#     logger.info("Get tool: %s", tool)
#
#
# @pytest.mark.asyncio
# async def test_read_main():
#     response = client.get("/")  # Используем await для асинхронного вызова
#     assert response.status_code == 200
#     assert response.json() == {"Check_conection": "OK"}
#
# @pytest.mark.asyncio
# def test_get_one_tool_invalid_id():
#     response = client.get("/abc")  # Неверный идентификатор
#     assert response.status_code == 404  # Проверяем, что статус ответа 404


#
# @pytest.fixture
# async def client(test_db):
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         yield client  # Возвращает клиент для тестов
#
#
# @pytest.mark.asyncio
# async def test_get_one_tool_found(client, test_db):
#     response = await client.get("/1")
#     assert response.status_code == 200
#     assert response.json()["name"] == "Test Drill"  # Проверьте, что имя соответствует
#
#
# @pytest.mark.asyncio
# async def test_get_one_tool_not_found(client):
#     response = await client.get("/999")  # Неизвестный tool_id
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Tool not found"
#
#
# @pytest.mark.asyncio
# async def test_get_one_tool_invalid_id(client):
#     response = await client.get("/abc")  # Неверный идентификатор
#     assert response.status_code == 422  # Неправильный тип данных
