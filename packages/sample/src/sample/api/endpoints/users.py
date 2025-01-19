from fastapi import APIRouter
from sqlmodel import select

from sample.api.deps import SessionDep
from sample.models.user import User
from sample.schemas.user import CreateUser, UserResponse
from sample.crud import user

router = APIRouter()


@router.get("")
def user_list(session: SessionDep):
    stmt = select(User.name).order_by(User.name)
    return session.exec(stmt).all()


@router.post("", response_model=UserResponse)
def create_user(request: CreateUser, session: SessionDep) -> UserResponse:
    return UserResponse.model_validate(user.create(session=session, create_user=request))


@router.delete("")
def delete_user():
    pass
