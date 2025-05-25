from collections.abc import Sequence

from sqlmodel import Session, select

from sample.models.user import User
from sample.schemas.user import CreateUser, UpdateUser


def user_list(*, session: Session) -> Sequence[User]:
    statement = select(User).order_by(User.name)
    return session.exec(statement).all()


def user_create(*, session: Session, create_user: CreateUser) -> User:
    db_obj = User.model_validate(create_user)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def user_delete(*, session: Session, user_id: int):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).one()
    session.delete(user)
    session.commit()


def get_user_by_id(*, session: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def user_update(*, session: Session, update_user: UpdateUser, user_id: int) -> User:
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).one()
    user_data = update_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    session.commit()
    session.refresh(user)
    return user
