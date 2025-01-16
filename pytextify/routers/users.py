from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pytextify.database import get_session
from pytextify.models import ConfirmationToken, User
from pytextify.schemas import Message, UserList, UserPublic, UserSchema
from pytextify.security import (
    get_current_user,
    get_password_hash,
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Message)
def create_user(
    user: UserSchema,
    session: T_Session,
):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.flush()

    confirmation_token = ConfirmationToken.generate_token(db_user.id)
    session.add(confirmation_token)
    session.commit()

    return {'message': 'Please check your email to confirm your registration.'}


@router.get('/confirm/{token}', response_model=Message)
def confirm_user(token: str, session: T_Session):
    confirmation_token = session.scalar(
        select(ConfirmationToken).where(ConfirmationToken.token == token)
    )

    if not confirmation_token:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Confirmation token not found',
        )

    if confirmation_token.is_used:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Confirmation token already used',
        )

    if confirmation_token.expires_at < confirmation_token.created_at:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Confirmation token expired',
        )

    confirmation_token.is_used = True
    confirmation_token.user.is_active = True
    session.commit()

    return {'message': 'User confirmed'}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only update your own user',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can only delete your own user',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session,
    _: T_CurrentUser,
    offset: int = 0,
    limit: int = 100,
):
    users = session.scalars(select(User).offset(offset).limit(limit))
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: T_Session, _: T_CurrentUser):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return db_user
