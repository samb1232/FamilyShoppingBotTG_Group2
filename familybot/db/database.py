import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


sync_engine = create_engine(
    url="sqlite:///database.db",
#    echo=True
)

session_factory = sessionmaker(sync_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
