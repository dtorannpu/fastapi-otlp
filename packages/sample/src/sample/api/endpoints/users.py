from fastapi import APIRouter, HTTPException

from sample.api.deps import SessionDep
from sample.crud import user
from sample.schemas.user import CreateUser, UpdateUser, UserResponse, UsersResponse

router = APIRouter()


@router.get("", response_model=UsersResponse)
async def user_list(session: SessionDep) -> UsersResponse:
    return UsersResponse.model_validate(await user.user_list(session=session))


@router.post("", response_model=UserResponse)
async def create_user(request: CreateUser, session: SessionDep) -> UserResponse:
    return UserResponse.model_validate(
        await user.user_create(session=session, create_user=request)
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, session: SessionDep) -> UserResponse:
    u = await user.get_user_by_id(session=session, user_id=user_id)
    if u is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(u)


@router.delete("{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    await user.user_delete(session=session, user_id=user_id)


@router.put("{user_id}", response_model=UserResponse)
async def update_user(
    request: UpdateUser, user_id: int, session: SessionDep
) -> UserResponse:
    return UserResponse.model_validate(
        await user.user_update(session=session, update_user=request, user_id=user_id)
    )
