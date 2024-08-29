import smtplib
from datetime import datetime
from email.message import EmailMessage

from celery import Celery
from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from auth.manager import fastapi_users
from config import settings

SMTP_HOST = settings.celery.smtp_host
SMTP_PORT = settings.celery.smtp_port
SMTP_USER = settings.celery.smtp_user  # email
SMTP_PASSWORD = settings.celery.smtp_password

celery = Celery(
    "tasks", broker=settings.redis.url, broker_connection_retry_on_startup=True
)


def get_email_template(name: str, email_to_send: str):
    email = EmailMessage()
    email["Subject"] = "Hello"
    email["From"] = SMTP_USER
    email["To"] = email_to_send

    email.set_content(
        f"""
        <html>
            <body>
                <p>Привет {name}, тестовое письмо </p>
                 "timestamp": {str(datetime.now())}
            </body>
        </html>
        """,
        subtype="html",
    )
    return email


@celery.task()
def send_email_test(name: str, email_to_send: str):
    email = get_email_template(name, email_to_send)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


router = APIRouter()
current_user = fastapi_users.current_user()


# celery -A y_project_services.task_celery.tasks:celery worker -l info
# poxers95@gmail.com
@router.get("/send-test-email-for-user")
async def send_email(background_tasks: BackgroundTasks, user=Depends(current_user)):

    # 1400 ms - Клиент ждет
    # flag = 'Sync method'
    # send_email_test(name=user.name, email_to_send=user.email)
    #
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    # flag = 'Async background method'
    # background_tasks.add_task(send_email_test, name=user.name, email_to_send=user.email)

    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    flag = "Async celery method"
    send_email_test.delay(name=user.name, email_to_send=user.email)

    return {
        "status": "ok",
        "method": flag,
        "data": "email sending",
        "detail": f"sending to: {user.name}, email: {user.email}",
        "timestamp": str(datetime.now()),
    }
