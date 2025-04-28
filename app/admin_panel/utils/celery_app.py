from celery import Celery

from core.config import CELERY_BROKER


celery = Celery(
    'tasks',
    broker=CELERY_BROKER,
    backend=CELERY_BROKER
)
