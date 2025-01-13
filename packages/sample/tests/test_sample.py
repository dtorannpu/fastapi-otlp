import factory
from sqlalchemy.orm import Session

from sample.database import get_engine
from sample.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("user_name")


def test1():
    users = UserFactory.create_batch(10000)
    with Session(get_engine()) as session:
        session.add_all(users)
        session.commit()
