from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    credits: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    confirmation_token: Mapped['ConfirmationToken'] = relationship(
        'ConfirmationToken', back_populates='user', uselist=False
    )


@table_registry.mapped_as_dataclass
class ConfirmationToken:
    __tablename__ = 'confirmation_tokens'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    token: Mapped[str]
    user_id: Mapped[int] = mapped_column(init=False, foreign_key='users.id')
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    expires_at: Mapped[datetime]
    is_used: Mapped[bool] = mapped_column(default=False)

    user: Mapped[User] = relationship(
        'User', back_populates='confirmation_token'
    )

    @classmethod
    def generate_token(cls, user_id, expiration_hours=24) -> str:
        return cls(
            token=str(uuid4()),
            user_id=user_id,
            expires_at=datetime.now() + timedelta(hours=expiration_hours),
        )

    def is_valid(self) -> bool:
        return not self.is_used and self.expires_at >= datetime.now()
