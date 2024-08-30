from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends

from auth.manager import fastapi_users
from project_services.task_celery.tasks import send_email_test


router = APIRouter()
current_user = fastapi_users.current_user()


# celery -A y_project_services.task_celery.tasks:celery worker -l info
# poxers95@gmail.com


@router.get("/send-test-email-for-user")
async def send_email(
    background_tasks: BackgroundTasks,
    msg: str | None = None,
    user=Depends(current_user),
):

    # 1400 ms - Клиент ждет
    # flag = 'Sync method'
    # send_email_test(name=user.name, email_to_send=user.email)

    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    # flag = 'Async background method'
    # background_tasks.add_task(send_email_test, name=user.name, email_to_send=user.email)

    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    flag = "Async celery method"
    send_email_test.delay(name=user.name, email_to_send=user.email, msg=msg)

    return {
        "status": "ok",
        "method": flag,
        "data": "email sending",
        "detail": f"sending to: {user.name}, email: {user.email}",
        "timestamp": str(datetime.now()),
    }
