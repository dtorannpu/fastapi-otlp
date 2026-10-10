from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sample.core.config import settings

url = f"postgresql+psycopg://{settings.db.username}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"
engine = create_async_engine(url, echo=True)
SessionLocal = async_sessionmaker(
    class_=AsyncSession, autoflush=False, expire_on_commit=False, bind=engine
)
