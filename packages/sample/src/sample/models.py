from sqlalchemy.orm import DeclarativeBase
from sqlmodel import SQLModel, Field


class Base(DeclarativeBase):
    pass


SQLModel.metadata = Base.metadata


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=30)
