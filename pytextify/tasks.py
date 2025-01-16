import base64
from datetime import datetime, timedelta
from io import BytesIO

import easyocr
from celery import Celery
from celery.result import AsyncResult
from celery.schedules import crontab
from PIL import Image
from redis import Redis

from pytextify.settings import Settings

settings = Settings()
celery_app = Celery(broker=settings.BROKER_URL, backend=settings.BACKEND_URL)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        clear_backend.s(),
        name='clear_redis',
    )


@celery_app.task
def extract_text_from_image(image_b64: str):
    image = Image.open(BytesIO(base64.b64decode(image_b64)))
    reader = easyocr.Reader(['en', 'pt'])
    result = reader.readtext(image)
    extracted_texts = [text for _, text, _ in result]
    return extracted_texts


@celery_app.task
def clear_backend():
    redis = Redis.from_url(settings.BACKEND_URL)
    for key in redis.keys('celery-task-meta-*'):
        task_id = key.decode('utf-8').replace('celery-task-meta-', '')
        task = AsyncResult(task_id, app=celery_app)
        if task.successful() and task.date_done < datetime.now() - timedelta(
            days=1
        ):
            redis.delete(key)
