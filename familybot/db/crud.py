# Create, read, update, delete! (orm queries)
from familybot.db.database import sync_engine, session_factory
from familybot.db.models import *


# Base
def create_tables() -> None:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


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


# Purchases
def get_family_purchases(family: Family) -> list[Purchase]:
    purchases = []

    for member in family.members:
        purchases.insert(-1, member.added_purchases)

    return purchases


def insert_purchase(purchases: list[Purchase]) -> None:
    with session_factory() as session:
        session.add_all(purchases)

        session.commit()


# Family
def create_family(host: Person) -> None:
    pass
