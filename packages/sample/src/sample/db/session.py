from sqlalchemy.orm import sessionmaker
from sqlmodel import Session as SQLModelSession
from sqlmodel import create_engine

from sample.core.config import settings

url = f"postgresql://{settings.db.username}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"
engine = create_engine(url, echo=True)
SessionLocal = sessionmaker(
    class_=SQLModelSession, autocommit=False, autoflush=False, bind=engine
)
