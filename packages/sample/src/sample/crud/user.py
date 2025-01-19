from typing import Sequence

from sqlmodel import Session, select

from sample.models.user import User
from sample.schemas.user import CreateUser


def get_all(*, session: Session) -> Sequence[User]:
    stmt = select(User).order_by(User.name)
    return session.exec(stmt).all()


def create(*, session: Session, create_user: CreateUser) -> User:
    db_obj = User.model_validate(create_user)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
