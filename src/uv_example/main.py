from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sample.models import Base, User


def main():
    engine = create_engine('sqlite:///test.db', echo=True)

    with Session(engine) as session:
        u1 = User(name='test1')
        u2 = User(name='test2')

        session.add_all([u1, u2])

        session.commit()


if __name__ == "__main__":
    main()
