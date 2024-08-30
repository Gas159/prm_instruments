import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from auth import router as router_v1_auth
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

for router in [
    router_v1_auth,
    router_v1_user,
    router_v1_service,
    router_v1_company,
]:
    main_app.include_router(router, prefix=settings.api.prefix)


add_pagination(main_app)




@main_app.get("/")
async def root():
    return {"data": "check"}


if __name__ == "__main__":
    uvicorn.run(
        "z_developer.main1:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        workers=3,
    )
