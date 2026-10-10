from typing import cast

import factory
import pytest
import pytest_asyncio
from factory import Faker
from sample.models.user import User
from sample.schemas.user import CreateUser, UpdateUser
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    name = Faker("name")


class CreateUserFactory(factory.Factory):
    class Meta:
        model = CreateUser

    name = Faker("name")


class UpdateUserFactory(factory.Factory):
    class Meta:
        model = UpdateUser

    name = Faker("name")


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
    # Factory Boyを使用してテストユーザーを作成
    users = [cast(User, UserFactory()) for _ in range(3)]
    for user in users:
        session.add(user)
    await session.commit()

    from sample.crud.user import user_list

    result = await user_list(session=session)

    assert len(result) == 3
    # nameでソートされていることを確認
    assert sorted([u.name for u in users]) == [u.name for u in result]


@pytest.mark.asyncio
async def test_user_create(session: AsyncSession):
    from sample.crud.user import user_create

    create_user_data = cast(CreateUser, CreateUserFactory())
    new_user = await user_create(session=session, create_user=create_user_data)

    assert new_user.id is not None
    assert new_user.name == create_user_data.name

    # データベースに保存されていることを確認
    db_user = await session.get(User, new_user.id)
    assert db_user is not None
    assert db_user.name == create_user_data.name


@pytest.mark.asyncio
async def test_user_delete(session: AsyncSession):
    from sample.crud.user import user_delete

    # Factory Boyでテストユーザーを作成
    user = cast(User, UserFactory())
    session.add(user)
    await session.commit()
    assert user.id is not None

    await user_delete(session=session, user_id=user.id)

    # 削除されたことを確認
    deleted_user = await session.get(User, user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    from sample.crud.user import get_user_by_id

    # Factory Boyでテストユーザーを作成
    user = cast(User, UserFactory())
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
    from sample.crud.user import user_update

    # Factory Boyでテストユーザーを作成
    user = cast(User, UserFactory())
    session.add(user)
    await session.commit()
    assert user.id is not None

    # 更新データをFactory Boyで生成
    update_data = cast(UpdateUser, UpdateUserFactory())
    updated_user = await user_update(
        session=session, update_user=update_data, user_id=user.id
    )

    assert updated_user.name == update_data.name

    # データベースで更新を確認
    db_user = await session.get(User, user.id)
    assert db_user is not None
    assert db_user.name == update_data.name
