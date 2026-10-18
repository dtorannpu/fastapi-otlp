from itertools import count

import pytest
import pytest_asyncio
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from sample.crud.user import (
    get_user_by_id,
    user_create,
    user_delete,
    user_list,
    user_update,
)
from sample.models.user import User
from sample.schemas.user import CreateUser, UpdateUser
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

_user_id_counter = count(1)


class UserFactory(ModelFactory[User]):
    id = Use(lambda: next(_user_id_counter))

    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


class CreateUserFactory(ModelFactory[CreateUser]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


class UpdateUserFactory(ModelFactory[UpdateUser]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_user_list(session: AsyncSession):
    # Polyfactoryを使用してテストユーザーを作成
    users = [UserFactory.build() for _ in range(3)]
    for user in users:
        session.add(user)
    await session.commit()

    result = await user_list(session=session)

    assert len(result) == 3
    # nameでソートされていることを確認
    assert sorted([u.name for u in users]) == [u.name for u in result]


@pytest.mark.asyncio
async def test_user_create(session: AsyncSession):
    create_user_data = CreateUserFactory.build()
    new_user = await user_create(session=session, create_user=create_user_data)

    assert new_user.id is not None
    assert new_user.name == create_user_data.name

    # データベースに保存されていることを確認
    db_user = await session.get(User, new_user.id)
    assert db_user is not None
    assert db_user.name == create_user_data.name


@pytest.mark.asyncio
async def test_user_delete(session: AsyncSession):
    # Polyfactoryでテストユーザーを作成
    user = UserFactory.build()
    session.add(user)
    await session.commit()
    assert user.id is not None

    await user_delete(session=session, user_id=user.id)

    # 削除されたことを確認
    deleted_user = await session.get(User, user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Polyfactoryでテストユーザーを作成
    user = UserFactory.build()
    session.add(user)
    await session.commit()
    assert user.id is not None

    # 存在するユーザーの取得
    found_user = await get_user_by_id(session=session, user_id=user.id)
    assert found_user is not None
    assert found_user.name == user.name

    # 存在しないユーザーの取得
    not_found_user = await get_user_by_id(session=session, user_id=999)
    assert not_found_user is None


@pytest.mark.asyncio
async def test_user_update(session: AsyncSession):
    # Polyfactoryでテストユーザーを作成
    user = UserFactory.build()
    session.add(user)
    await session.commit()
    assert user.id is not None

    # 更新データをPolyfactoryで生成
    update_data = UpdateUserFactory.build()
    updated_user = await user_update(
        session=session, update_user=update_data, user_id=user.id
    )

    assert updated_user.name == update_data.name

    # データベースで更新を確認
    db_user = await session.get(User, user.id)
    assert db_user is not None
    assert db_user.name == update_data.name
