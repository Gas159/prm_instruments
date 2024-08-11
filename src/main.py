from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException
import uvicorn
from fastapi.responses import ORJSONResponse
# from pydantic import ValidationError
# from starlette.requests import Request
# from starlette.responses import JSONResponse

from api.v1 import router as api_v1_router
from config import settings
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


@main_app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return ORJSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )



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
    return {"data": "i18n"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
