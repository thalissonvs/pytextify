from enum import Enum
from http import HTTPStatus

from celery.result import AsyncResult
from fastapi import FastAPI

from pytextify.schemas import ImageSchema, TaskResultSchema, TaskSchema
from pytextify.tasks import celery_app, extract_text_from_image

app = FastAPI()


class TaskStatus(str, Enum):
    PROCESSING = 'processing'
    DONE = 'done'
    FAILED = 'failed'


@app.post(
    '/textify', response_model=TaskSchema, status_code=HTTPStatus.ACCEPTED
)
def convert_image_to_text(image: ImageSchema):
    result = extract_text_from_image.delay(image.image_base64)
    return {'task_id': result.id, 'status': TaskStatus.PROCESSING}


@app.get('/textify/{task_id}', response_model=TaskResultSchema)
def get_task_result(task_id: str):
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


# TODO: Criar sistema de autenticação
# TODO: Criar sistema de rate limit
# TODO: Adicionar limite de quantas tarefas cada usuário pode solicitar ao mesmo tempo
# TODO: Adicionar limite de tamanho de imagem
# TODO: Criar Enums para os status das tarefas
# TODO: Adicionar testes
# TODO: Documentação
# TODO: Logging com Loki
# TODO: Monitoramento com Prometheus
# TODO: Adicionar rabbit e redis no docker-compose
# TODO: Adicionar CI/CD
# TODO: Adicionar cache
# TODO: Adicionar nginx como servidor no docker-compose
# TODO: Adicionar sistema de créditos para os usuários
# TODO: Usar celery beat para agendar tarefa de limpeza de tarefas antigas
# TODO: Adicionar sistema de notificação por email
