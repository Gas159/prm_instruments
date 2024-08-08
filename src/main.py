from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from fastapi.responses import ORJSONResponse

from api.v1 import router as api_v1_router
from config import settings
from database import db_helper
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
            # print("create engine")
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    # improve speed work with db
    default_response_class=ORJSONResponse,
)
main_app.include_router(
    api_v1_router,
    prefix=settings.api.prefix,
    # mainApp.mount("/app", app)  # your app routes will now be /app/{your-route-here}
)

origins = [
    # "http://localhost:3000",
    # "https://car-service-18635.web.app",
    # "https://*",
    # "http://*",
    "*",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@main_app.get("/")
async def root():
    return {"data": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
    # import uvicorn.workers.UvicornWorker
    # uvicorn.run(   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001 --reload )
