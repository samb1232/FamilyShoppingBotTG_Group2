# Create, read, update, delete! (orm queries)
from sqlalchemy import inspect, exc
from familybot.db.database import sync_engine, session_factory
from familybot.db.models import *


# Base
def create_tables() -> None:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def init_tables() -> bool:  # Returns False if tables don't exist
    if inspect(sync_engine).has_table("families") or \
            inspect(sync_engine).has_table("purchases") or \
            inspect(sync_engine).has_table("persons"):
        return True

    create_tables()

    return False


# Persons
def insert_persons(users: list[Person]) -> None:
    with session_factory() as session:
        session.add_all(users)

        session.commit()


def get_all_persons() -> list[Person]:
    with session_factory() as session:
        return session.query(Person).all()


def get_person_by_tg(tag: str) -> Person | None:
    with session_factory() as session:
        try:
            return session.query(Person).where(Person.telegram_id == tag).one()
        except exc.NoResultFound as err:
            return None
    

def get_person_by_id(pid: int) -> Person:
    with session_factory() as session:
        return session.query(Person).get(pid)


# Purchases
def insert_purchase(purchases: list[Purchase]) -> None:
    with session_factory() as session:
        session.add_all(purchases)

        session.commit()


def get_all_purchases() -> list[Purchase]:
    with session_factory() as session:
        return session.query(Purchase).all()


# Families
def get_all_families() -> list[Family]:
    with session_factory() as session:
        return session.query(Family).all()
