import os
import time
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('api_tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='api_tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y

celery.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'api_tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

celery.conf.timezone = 'UTC'
