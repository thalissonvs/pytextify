from fastapi import FastAPI

from pytextify.routers import auth, textify, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(textify.router)
app.include_router(users.router)


# TODO: Adicionar sistema de enviar email para confirmar cadastro
"""
O envio de email será seguida a seguinte abordagem:
- Criação de tabela para armazenar os tokens de confirmação
- Campo 'is_active' na tabela de usuários
- Tarefa periódica com celery beat para limpar tokens expirados
- Cadastro irá gerar um token de confirmação e enviar um email com o link
- Ao clicar no link, o token será verificado e o usuário será ativado
- Envio de e-mail com uma task do celery
- Ativação do cadastro irá adicionar créditos ao usuário
"""
# TODO: Adicionar campo 'credits' na tabela de usuários
# TODO: Atualizar campo 'credits' diariamente para reposição com celery beat
# TODO: Criar sistema de rate limit
# TODO: Adicionar limite de quantas tasks cada usuário pode solicitar
# TODO: Adicionar limite de tamanho de imagem
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
