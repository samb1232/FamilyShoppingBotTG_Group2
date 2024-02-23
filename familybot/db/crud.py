# Create, read, update, delete! (orm queries)
from sqlalchemy import inspect
from familybot.db.database import sync_engine, session_factory
from familybot.db.models import *


# Base
def create_tables() -> None:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def init_tables() -> bool:  # Returns False if tables don't exist
    if not inspect(sync_engine).has_table("clients") or \
            not inspect(sync_engine).has_table("purchases") or \
            not inspect(sync_engine).has_table("notes"):
        create_tables()
        return False

    return True


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
        return session.query(Person).where(Person.telegram_tag == tag).one()
    

def get_person_by_id(id: int) -> Person:
    with session_factory() as session:
        return session.query(Person).get(id)


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
