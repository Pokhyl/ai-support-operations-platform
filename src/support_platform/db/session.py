import os

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine


def build_database_url() -> URL:
    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ["DB_NAME"],
    )


def create_database_engine() -> Engine:
    return create_engine(
        build_database_url(),
        pool_pre_ping=True,
    )
