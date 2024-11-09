import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import main_app as app
from tools.drills.models import DrillModel

client = TestClient(app)


# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World1"}
#
#
# # Пример использования `patch` для обхода зависимостей
# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Check_conection": "OK"}


# @pytest.mark.asyncio
# async def test_get_one_drill_found(session: AsyncSession):
#     # Arrange
#     drill = DrillModel(id=1)
#     session.add(drill)
#     await session.commit()
#
#     # Act
#     response = client.get(f"/{drill.id}")
#
#     # Assert
#     assert response.status_code == 200
#     assert response.json()["id"] == drill.id


#
# @pytest.mark.asyncio
# async def test_get_one_drill_not_found(session: AsyncSession):
#     # Act
#     response = client.get("/1")
#
#     # Assert
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Tool not found"
#
#
# @pytest.mark.asyncio
# async def test_get_one_invalid_tool_id():
#     # Act
#     response = client.get("/abc")
#
#     # Assert
#     assert response.status_code == 422
#
#
# @pytest.mark.asyncio
# async def test_get_one_tool_id_is_none():
#     # Act
#     response = client.get("/")
#
#     # Assert
#     assert response.status_code == 422
