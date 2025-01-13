from sqlalchemy import select
from sqlalchemy.orm import Session

from sample.database import get_engine
from sample.models import User


class UserRepository:
    @staticmethod
    def get_all_name():
        with Session(get_engine()) as session:
            stmt = select(User.name).order_by(User.name.asc())
            return session.execute(stmt).scalars().all()
