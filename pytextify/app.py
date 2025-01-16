from fastapi import FastAPI

from pytextify.routers import auth, textify, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(textify.router)
app.include_router(users.router)


# TODO: Criar sistema de autenticação
# TODO: Criar sistema de rate limit
# TODO: Adicionar limite de quantas tasks cada usuário pode solicitar
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
