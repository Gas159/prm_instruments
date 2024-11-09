import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from main import main_app as app  # Импортируйте ваш FastAPI-приложение
from tools.drills.models import DrillModel

client = TestClient(app)

# @pytest.mark.asyncio
# async def test_drill_model(get_session):
# 	"""
# 	Тестируем модель DrillModel.
# 	Проверяем, что запись была успешно создана и доступна в базе данных.
# 	"""
# 	async with   get_session as session:
# 		result = await session.execute(select(DrillModel).where(DrillModel.name == 'Test Drill'))
# 		drill = result.scalar_one_or_none()
#
# 		assert drill is not None
# 		assert drill.name == 'Test Drill'