from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session as SQLModelSession

from sample.db.session import SessionLocal


def get_session() -> Generator:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[SQLModelSession, Depends(get_session)]
