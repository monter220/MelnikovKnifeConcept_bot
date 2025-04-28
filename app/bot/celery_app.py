import asyncio

from celery import Celery

from handler_delayed_message import send_delayed_message
from config import settings


celery = Celery(
    'tasks',
    broker=settings.bot.celery_broker,
    backend=settings.bot.celery_broker
)
celery.conf.broker_connection_retry_on_startup = True


@celery.task(name='tasks.delayed_message')
def delayed_message(message_id: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_delayed_message(message_id))