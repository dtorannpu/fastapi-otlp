from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from sample.db.session import SessionLocal

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
