import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from starlette.staticfiles import StaticFiles

from config import settings
from exceptions import validation_exception_handler, internal_server_error
from project_services.cors import add_cors_middleware
from project_services.llifespan import lifespan

from tools.drills import router as router_drills
from tools.archive.drills import router as router_drills_archive
from tools.drills.cruds import UPLOAD_DIR

main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # improve speed work with db
)
# Настройка маршрутов для статических файлов
main_app.mount("/static", StaticFiles(directory="static"), name="static")
main_app.add_exception_handler(500, internal_server_error)
main_app.add_exception_handler(422, validation_exception_handler)


# Добавляем путь для статических файлов
main_app.mount(
    "/uploaded_images", StaticFiles(directory=UPLOAD_DIR), name="uploaded_images"
)

for router in [router_drills, router_drills_archive]:
    main_app.include_router(router)

# add cors
add_cors_middleware(main_app)

add_pagination(main_app)
# templates = Jinja2Templates(directory="templates")


@main_app.get("/")
async def get_homepage():
    return {"Check_conection": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        workers=3,
    )
