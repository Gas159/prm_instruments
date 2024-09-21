from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from starlette.requests import Request
from starlette.responses import FileResponse
from config import settings

from fastapi.templating import Jinja2Templates

# from auth.app import router as router_v1_auth
# from companies import router as router_v1_company
# from services import router as router_v1_service
# from users import router as router_v1_user
from osnastka import router as router_v1_utils
from exceptions import validation_exception_handler, internal_server_error
from project_services.cors import add_cors_middleware
from project_services.llifespan import lifespan
from project_services.task_celery.router import router as router_v1_task

main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # improve speed work with db
)

main_app.add_exception_handler(500, internal_server_error)
main_app.add_exception_handler(422, validation_exception_handler)

for router in [
    # router_v1_auth,
    # router_v1_user,
    # router_v1_service,
    # router_v1_company,
    # router_v1_task,
    router_v1_utils
]:
    # main_app.include_router(router, prefix=settings.api.prefix)
    main_app.include_router(router)

# add cors
add_cors_middleware(main_app)

add_pagination(main_app)
# templates = Jinja2Templates(directory="templates")

# @main_app.get("/")
# async def root():
#     return {"data": "check"}


# @main_app.get("/", response_class=FileResponse)
# async def get_homepage(request: Request):
#     return FileResponse("templates/index.html")
# @main_app.get("/1", response_class=FileResponse)
# async def get_homepage(request: Request):
#     return FileResponse("templates/base.html")


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        workers=3,
    )
