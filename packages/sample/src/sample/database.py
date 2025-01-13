import os

from sqlalchemy import create_engine, Engine


def get_engine() -> Engine:
    return create_engine(
        f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT_OUTER')}/{os.getenv('DB_NAME')}",
        echo=True,
    )
