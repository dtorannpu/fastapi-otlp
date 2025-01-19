from sqlmodel import Session

from sample.models.user import User
from sample.schemas.user import CreateUser


def create(*, session: Session, create_user: CreateUser) -> User:
    db_obj = User.model_validate(create_user)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
