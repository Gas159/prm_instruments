import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Общий уровень логирования
    format="%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(process)d - %(threadName)s - %(message)s",
    handlers=[
        # logging.FileHandler("app.log"),  # Логи записываются в файл
        logging.StreamHandler(),  # Логи выводятся на консоль
    ],
)
logging.getLogger("multipart").setLevel(logging.INFO)


upload_dir = Path("uploaded_images")


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8003


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/user"
    services: str = "/service"
    companies: str = "/company"
    auth: str = "/auth"
    auth_jwt: str = "/auth/jwt"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


# url: str = 'postgresql+asyncpg://gas:123@localhost:5432/shop'
class DatabaseConfig(BaseModel):
    url: PostgresDsn
    postgres_user: str
    postgres_password: str
    postgres_db: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class CeleryConfig(BaseModel):
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_password: str
    smtp_user: str


class RedisConfig(BaseModel):
    url: str = "redis://localhost:6379"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        # env_file=(".env", ".env.template", ".env.local"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    celery: CeleryConfig
    redis: RedisConfig = RedisConfig()


settings = Settings()
print(settings.db.url)
print(settings.db.echo)
print(settings.db.echo_pool)
