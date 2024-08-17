import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from services import router as router_v1_service
from companies import router as router_v1_company
from users import router as router_v1_user

from config import settings
from project_services.llifespan import lifespan
from exceptions import validation_exception_handler, internal_server_error

main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # improve speed work with db
)

main_app.add_exception_handler(500, internal_server_error)
main_app.add_exception_handler(422, validation_exception_handler)

main_app.include_router(
    router_v1_service,
    prefix=settings.api.prefix,
)
main_app.include_router(
    router_v1_company,
    prefix=settings.api.prefix,
)

main_app.include_router(
    router_v1_user,
    prefix=settings.api.prefix,
)

add_pagination(main_app)


@main_app.get("/")
async def root():
    return {"data": "check"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        workers=3,
    )
