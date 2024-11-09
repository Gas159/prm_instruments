import smtplib
from datetime import datetime
from email.message import EmailMessage

from celery import Celery
from config import settings

SMTP_HOST = settings.celery.smtp_host
SMTP_PORT = settings.celery.smtp_port
SMTP_USER = settings.celery.smtp_user  # email
SMTP_PASSWORD = settings.celery.smtp_password

celery = Celery("tasks", broker=settings.redis.url, broker_connection_retry_on_startup=True)


def get_email_template(name: str, email_to_send: str, msg: str | None):
    email = EmailMessage()
    email["Subject"] = "Hello"
    email["From"] = SMTP_USER
    email["To"] = email_to_send

    email.set_content(
        f"""
        <html>
            <body>
             <p> {msg} </p>
                <p>Привет {name}, это тестовое письмо </p>
               
                 "timestamp": {str(datetime.now())}
            </body>
        </html>
        """,
        subtype="html",
    )
    return email


@celery.task
def send_email_test(name: str, email_to_send: str, msg: str | None = None):
    email = get_email_template(name, email_to_send, msg)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


# router = APIRouter()
# current_user = fastapi_users.current_user()


# celery -A y_project_services.task_celery.tasks:celery worker -l info
# poxers95@gmail.com
