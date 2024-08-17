from starlette.middleware.cors import CORSMiddleware

from main import main_app

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
