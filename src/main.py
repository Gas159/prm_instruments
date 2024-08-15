import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from api import router as api_v1_router_v1
from api.v1 import router as api_v1_router
from config import settings
from database import lifespan
from exceptions import validation_exception_handler, internal_server_error

main_app = FastAPI(
    lifespan=lifespan,
    # improve speed work with db
    default_response_class=ORJSONResponse,
)

main_app.add_exception_handler(500, internal_server_error)
main_app.add_exception_handler(422, validation_exception_handler)

main_app.include_router(
    api_v1_router,
    prefix=settings.api.prefix,
    # mainApp.mount("/app", app)  # your app routes will now be /app/{your-route-here}
)
main_app.include_router(
    api_v1_router_v1,
    prefix=settings.api.prefix,
    # mainApp.mount("/app", app)  # your app routes will now be /app/{your-route-here}
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
