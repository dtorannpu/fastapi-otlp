from fastapi import APIRouter
from sqlmodel import select

from sample.api.deps import SessionDep
from sample.models import User
from sample.schemas import CreateUser

router = APIRouter()


@router.get("")
def user_list(session: SessionDep):
    stmt = select(User.name).order_by(User.name)
    return session.exec(stmt).all()


@router.post("")
def create_user(request: CreateUser):
    return request


@router.delete("")
def delete_user():
    pass
