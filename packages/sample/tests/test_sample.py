import factory

from sample.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("user_name")


def test1():
    # users = UserFactory.create_batch(10000)
    # engine = create_engine('sqlite:///../../../test.db', echo=True)
    # with Session(engine) as session:
    #     session.add_all(users)
    #     session.commit()
    pass
