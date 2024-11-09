from tracemalloc import Statistic

import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine, StaticPool
from websockets.asyncio.client import connect

from project_services.base import Base  # Импортируем модели из вашего проекта
from tools.drills.models import DrillModel

# Настройка подключения к базе данных
# DB_URL = "sqlite:///:memory:"
# engine = create_engine(DB_URL,
#                        connect={"check_same_thread": False},
#                        poolclass=StaticPool,
#                        echo=True,)
# TestingSessionLocal = sessionmaker(bind=engine,
#                                    autoflush=False,
#                                    autocommit=False,
#                                    expire_on_commit=False,)
#
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture(scope="module")
# async def init_test_database():
#     """
#     Инициализация базы данных перед началом тестирования.
#     Создаем таблицы и заполняем их данными.
#     """
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     async with async_session_factory() as session:
#         async with session.begin():
#             drill = DrillModel(name="Test Drill")
#             session.add(drill)
#             await session.commit()
#
#     yield
#
#     # Очистка базы данных после завершения тестов
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# @pytest.fixture
# async def get_session(init_test_database):
#     """
#     Фикстура для получения сессии базы данных.
#     Используется в каждом тесте для взаимодействия с базой данных.
#     """
#     async with async_session_factory() as session:
#         async with session.begin():
#             yield session