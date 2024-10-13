from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request


async def internal_server_error(request: Request, exc: Exception):
    # logger.error(f"Internal Server Error: {exc}")
    return ORJSONResponse(
        status_code=500,
        content={
            "error": "Internal server error!",
            "request_url": str(request.url),  # Только URL запроса
            "request_method": request.method,
            "detail": str(exc),
            "traceback": str(exc.__traceback__),
            "request": str(request),
            "body": str(request.body),
            "headers": str(request.headers),
            "cookies": str(request.cookies),
            "query_params": str(request.query_params),
            "path_params": str(request.path_params),
        },
    )


# @main_app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return ORJSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "request": str(request.url),
            "body": exc.body,
        },
    )
