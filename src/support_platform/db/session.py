import os
from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


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


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    engine = create_database_engine()

    return sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
    )


def get_db() -> Generator[Session, None, None]:
    db = get_session_factory()()

    try:
        yield db
    finally:
        db.close()