from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

from fastapi.exceptions import ValidationException
import uvicorn
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from fastapi_users import FastAPIUsers

from api.v1 import router as api_v1_router
from auth.auth import auth_backend
from auth.database import User

from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
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

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
main_app.include_router(
    fastapi_users.get_auth_router(
        auth_backend
    ),  # add  requires_verification=True if need check verify
    prefix="/auth/jwt",
    tags=["auth"],
)

main_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


add_pagination(main_app)


@main_app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return ORJSONResponse(status_code=422, content={"detail": exc.errors()})


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
    return {"data": "i18n"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
