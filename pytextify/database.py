from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pytextify.settings import Settings

engine = create_engine(Settings().DATABASE_URL, echo=True)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
