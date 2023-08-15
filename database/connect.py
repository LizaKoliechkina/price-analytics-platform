import os
from uuid import uuid4

import typing
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def generate_uuid() -> str:
    return uuid4().hex


DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_session() -> typing.Iterator:
    db = Session()
    try:
        yield db
    finally:
        db.close()
