import smtplib
from email.message import EmailMessage

from celery import Celery
from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from auth.manager import fastapi_users
# from auth.auth import fastapi_users
from config import settings
from y_project_services.redis_tools import redis


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "pankot222@gmail.com"

SMTP_PASSWORD = settings.celery.SMTP_PASSWORD  # SMTP_PASSWORD = "zbvt vipx gzws fiod"
celery = Celery(
    "tasks", broker="redis://localhost:6379", broker_connection_retry_on_startup=True
)


def get_email_template(username: str):
    email = EmailMessage()
    email["Subject"] = "Hello"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        f"""
        <html>
            <body>
                <p>Привет {username}</p>
            </body>
        </html>
        """,
        subtype="html",
    )
    return email


# @celery.task
def send_email_test(username: str):
    email = get_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

current_user = fastapi_users.current_user()


@router.get("/dashboard")
async def get_dashboard(background_tasks: BackgroundTasks, user=Depends(current_user)):
    background_tasks.add_task(send_email_test, user.username)
    send_email_test(user.username)
    return {"status": "ok", "data": "email sending", "detail": None}
