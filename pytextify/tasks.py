import base64
from io import BytesIO

import easyocr
from celery import Celery
from PIL import Image

from pytextify.settings import Settings

settings = Settings()

celery_app = Celery(broker=settings.BROKER_URL, backend=settings.BACKEND_URL)


@celery_app.task
def extract_text_from_image(image_b64: str):
    image = Image.open(BytesIO(base64.b64decode(image_b64)))
    reader = easyocr.Reader(['en', 'pt'])
    result = reader.readtext(image)
    extracted_texts = [text for _, text, _ in result]
    return extracted_texts
