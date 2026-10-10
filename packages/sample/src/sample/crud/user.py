from typing import TYPE_CHECKING

from sqlmodel import select

from sample.models.user import User

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlmodel.ext.asyncio.session import AsyncSession

    from sample.schemas.user import CreateUser, UpdateUser


async def user_list(*, session: AsyncSession) -> Sequence[User]:
    statement = select(User).order_by(User.name)
    return (await session.exec(statement)).all()


async def user_create(*, session: AsyncSession, create_user: CreateUser) -> User:
    db_obj = User.model_validate(create_user)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def user_delete(*, session: AsyncSession, user_id: int) -> None:
    statement = select(User).where(User.id == user_id)
    user = (await session.exec(statement)).one()
    await session.delete(user)
    await session.commit()


async def get_user_by_id(*, session: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    return (await session.exec(statement)).first()


async def user_update(
    *, session: AsyncSession, update_user: UpdateUser, user_id: int
) -> User:
    statement = select(User).where(User.id == user_id)
    user = (await session.exec(statement)).one()
    user_data = update_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    await session.commit()
    await session.refresh(user)
    return user
