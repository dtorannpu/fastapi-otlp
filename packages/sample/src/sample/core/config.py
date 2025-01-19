import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class DatabaseSettings(BaseModel):
    host: str
    port: str
    username: str
    password: str
    name: str


class Settings(BaseModel):
    db: DatabaseSettings


def get_env_var(key: str):
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable '{key}' is missing.")
    return value


host = get_env_var("DB_HOST")
username = get_env_var("DB_USERNAME")
password = get_env_var("DB_PASSWORD")
name = get_env_var("DB_NAME")
port = get_env_var("DB_PORT")

settings = Settings(
    db=DatabaseSettings(
        host=host,
        username=username,
        password=password,
        name=name,
        port=port,
    )
)
