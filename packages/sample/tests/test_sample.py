import factory
from sample.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('user_name')


def test1():
    users = UserFactory.create_batch(10)
    for user in users:
        print(user.name)
