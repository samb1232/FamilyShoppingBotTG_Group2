import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

sync_engine = create_engine(
    url=os.environ.get("DATABASE_URL"),
    echo=False
)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
