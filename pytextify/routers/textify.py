from http import HTTPStatus
from typing import Annotated

from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from pytextify.enums import TaskStatus
from pytextify.models import User
from pytextify.schemas import ImageSchema, TaskResultSchema, TaskSchema
from pytextify.security import get_current_user
from pytextify.tasks import celery_app, extract_text_from_image

router = APIRouter(prefix='/textify', tags=['textify'])


T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/textify', response_model=TaskSchema, status_code=HTTPStatus.ACCEPTED
)
def convert_image_to_text(image: ImageSchema, _: T_CurrentUser):
    result = extract_text_from_image.delay(image.image_base64)
    return {'task_id': result.id, 'status': TaskStatus.PROCESSING}


@router.get('/textify/{task_id}', response_model=TaskResultSchema)
def get_task_result(task_id: str, _: T_CurrentUser):
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        task_result = result.result if result.successful() else result.info
        task_status = (
            TaskStatus.DONE if result.successful() else TaskStatus.FAILED
        )
        return {
            'task_id': task_id,
            'status': task_status,
            'result': task_result,
        }
    return {'task_id': task_id, 'status': 'processing'}
