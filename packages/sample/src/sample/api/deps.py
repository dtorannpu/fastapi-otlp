from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import Session as SQLModelSession

from sample.db.session import SessionLocal


def get_session() -> Generator:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[SQLModelSession, Depends(get_session)]
