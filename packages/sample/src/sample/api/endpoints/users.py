from fastapi import APIRouter

from sample.api.deps import SessionDep
from sample.crud import user
from sample.schemas.user import CreateUser, UserResponse, UsersResponse

router = APIRouter()


@router.get("", response_model=UsersResponse)
def user_list(session: SessionDep) -> UsersResponse:
    return UsersResponse.model_validate(user.get_all(session=session))


@router.post("", response_model=UserResponse)
def create_user(request: CreateUser, session: SessionDep) -> UserResponse:
    return UserResponse.model_validate(
        user.create(session=session, create_user=request)
    )


@router.delete("")
def delete_user():
    pass
