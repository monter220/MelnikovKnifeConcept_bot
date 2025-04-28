from celery.result import AsyncResult

from .celery_app import celery
from .app_time import current_time_with_timezone, make_datetime_timezone_aware


def create_task(message):
    """Создает задачу для отложенного сообщения в Celery."""
    message_date = make_datetime_timezone_aware(message.datetime)
    delay = message_date - current_time_with_timezone()
    delay = delay.total_seconds()
    task = celery.send_task('tasks.delayed_message',
                            kwargs={'message_id': str(message.id)},
                            countdown=delay)
    message.id_celery = task.id
    message.save()


def delete_task(message):
    """Удаляет задачу для отложенного сообщения в Celery."""
    if message.id_celery:
        task_result = AsyncResult(message.id_celery, app=celery)
        task_result.revoke(terminate=True)
