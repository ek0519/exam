from functools import lru_cache

from sqlmodel import Session

import config
from app.database import engine, create_db_and_tables
from . import create_app


def get_session():
    with Session(engine) as session:
        yield session


@lru_cache()
def get_settings():
    return config.Settings()


app = create_app()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
