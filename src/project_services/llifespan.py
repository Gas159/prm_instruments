from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    # from models import Base
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    # await conn.run_sync(Base.metadata.create_all)
    # print("create engine")
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()