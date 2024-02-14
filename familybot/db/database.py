import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


load_dotenv(find_dotenv())

sync_engine = create_engine(
    url=os.environ.get("DB_URL"),
    echo=False
)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
