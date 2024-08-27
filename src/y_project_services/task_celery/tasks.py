import smtplib
from email.message import EmailMessage

from celery import Celery
from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks
from auth.manager import fastapi_users
from config import settings


SMTP_HOST = settings.celery.smtp_host
SMTP_PORT = settings.celery.smtp_port
smtp_user = settings.celery.smtp_user  # email
SMTP_PASSWORD = settings.celery.smtp_password
#
# celery = Celery(
#     "tasks", broker="redis://localhost:6379",
# )
# SMTP_HOST = "smtp.gmail.com"
# SMTP_PORT = 465
# SMTP_USER = "pankot222@gmail.com"
# SMTP_PASSWORD = settings.celery.smtp_password

celery = Celery(
    "tasks", broker=settings.redis.url, broker_connection_retry_on_startup=True
)


def get_email_template(username: str, smtp_user: str):
    email = EmailMessage()
    email["Subject"] = "Hello"
    email["From"] = smtp_user
    email["To"] = smtp_user

    email.set_content(
        f"""
        <html>
            <body>
                <p>Привет {username}, тестовое письмо </p>
            </body>
        </html>
        """,
        subtype="html",
    )
    return email


# @celery.task
def send_email_test(username: str, email: str | None = None):
    if not email is None:
        smtp_user = email
    email = get_email_template(username, smtp_user)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(smtp_user, SMTP_PASSWORD)
        server.send_message(email)


router = APIRouter(
    prefix=settings.api.prefix,
)

current_user = fastapi_users.current_user()


@router.get("/send-test-email-for-user")
async def send_test_email_for_user(
    background_tasks: BackgroundTasks, user=Depends(current_user), email: str = None
):

    background_tasks.add_task(send_email_test, user.username, email)
    send_email_test(user.username, email)
    return {
        "status": "ok",
        "data": "email sending",
        "detail": f"sending to {user.username}",
    }
