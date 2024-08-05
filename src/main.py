from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from api import router as api_router
from config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()

#1
main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
    # mainApp.mount("/app", app)  # your app routes will now be /app/{your-route-here}
)


@main_app.get("/")
async def root():
    return {"data": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
