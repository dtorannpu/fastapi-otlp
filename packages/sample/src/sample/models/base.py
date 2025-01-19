from sqlalchemy.orm import DeclarativeBase
from sqlmodel import SQLModel


class Base(DeclarativeBase):
    pass


SQLModel.metadata = Base.metadata