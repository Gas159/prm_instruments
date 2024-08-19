import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from auth import router as router_v1_auth
from companies import router as router_v1_company
from config import settings
from exceptions import validation_exception_handler, internal_server_error
from services import router as router_v1_service
from users import router as router_v1_user
from z_project_services.cors import add_cors_middleware
from z_project_services.llifespan import lifespan

main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # improve speed work with db
)

main_app.add_exception_handler(500, internal_server_error)
main_app.add_exception_handler(422, validation_exception_handler)

for router in [
    router_v1_auth,
    router_v1_user,
    router_v1_service,
    router_v1_company,
]:
    main_app.include_router(router, prefix=settings.api.prefix)

# add cors
add_cors_middleware(main_app)

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
