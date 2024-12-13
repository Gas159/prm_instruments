import asyncio
import logging
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from config import settings
from project_services.base import Base
from tools.drills_monolit.models import DrillMonolitModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
db_url = config.get_main_option("sqlalchemy.url")
# alembic -c alembic.ini -n alembic:test upgrade head


if db_url:
    db_url = db_url
else:
    db_url = str(settings.db.url)

config.set_main_option("sqlalchemy.url", db_url)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from companies.models import CompanyModel  # Импорт модели компании
from services.models import ServiceModel  # Импорт модели сервиса
from users.models import UserModel  # Импорт модели пользователя

from tools.drills.models import DrillModel
from tools.archive.drills.models import DrillArchiveModel
from tools.screws.models import ScrewModel

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
# config.set_main_option("sqlalchemy.url", str(settings.db.url))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
