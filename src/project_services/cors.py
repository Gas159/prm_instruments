from starlette.middleware.cors import CORSMiddleware


origins = [
    # "http://localhost:8003",
    # "https://car-service-18635.web.app",
    # "https://*",
    # "http://*",
    # "*",
    "http://localhost:5173",  # Локальный фронтенд
    "https://gas159.ru",
]


def add_cors_middleware(app):
    app.add_middleware(
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
            "Access-Control-Allow-Credentials",
        ],
    )
