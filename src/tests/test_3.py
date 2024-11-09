from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from main import main_app as app
from database import db_helper

from project_services.base import Base  # Импортируем модели из вашего проекта

# Настройка подключения к базе данных
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool,
                       echo=True,)
TestingSessionLocal = sessionmaker(bind=engine,
                                   autoflush=False,
                                   autocommit=False,
                                   expire_on_commit=False,)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[db_helper.session_getter] = override_get_db

def setup():
	Base.metadata.create_all(bind=engine)
	session = TestingSessionLocal()
	# session.add(DrillModel(name="Test Drill"))
	# session.commit()
	# session.close()

def teardown():
    Base.metadata.drop_all(bind=engine)

@app.get("/")
async def read_main():
    return {"msg": "Hello World1"}

# Пример использования `patch` для обхода зависимостей
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Check_conection": "OK"}


async def test_drill_model():
    response = client.post('/drill/create', json={'name': 'Test Drill'})
    # result =  session.execute(select(DrillModel).where(DrillModel.name == 'Test Drill'))
    # drill = result.scalar_one_or_none()

    assert drill is not None
    assert drill.name == 'Test Drill'