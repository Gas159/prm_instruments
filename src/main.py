from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse

from fastapi_pagination import add_pagination

from auth.app import router as router_v1_auth
from companies import router as router_v1_company
from config import settings
from exceptions import validation_exception_handler, internal_server_error
from services import router as router_v1_service
from users import router as router_v1_user
from y_project_services.task_celery.tasks import router as router_v1_task
from y_project_services.cors import add_cors_middleware
from y_project_services.llifespan import lifespan

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
    router_v1_task,
]:
    main_app.include_router(router, prefix=settings.api.prefix)

# add cors
add_cors_middleware(main_app)

add_pagination(main_app)


@main_app.get("/")
async def root():
    return {"data": "check"}


# @main_app.post("/login")
# def login(form_data: Annotated[UserLogin, Depends()]):
#     data = form_data.model_dump()
#     # data["scopes"] = []
#     # for scope in form_data.scopes:
#     #     data["scopes"].append(scope)
#     # if form_data.client_id:
#     #     data["client_id"] = form_data.client_id
#     # if form_data.client_secret:
#     #     data["client_secret"] = form_data.client_secret
#     return data


# current_user = fastapi_users.current_user()
# @main_app.get("/current_user")
# async def protected_route(user=Depends(current_user)):
#     return {"status": "ok", "data": "email sending", "detail": None, 'user': user.username}
#
#
# @main_app.post("/login")
# async def login(request: Request, response: Response, user: User = Depends(fastapi_users.get_current_user)):
#     # Пример получения токена
#     token = await fastapi_users.get_login_response(user)
#     response.set_cookie(key="access_token", value=token.access_token, max_age=3600)
#     return {"message": "Login successful"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        workers=3,
    )
