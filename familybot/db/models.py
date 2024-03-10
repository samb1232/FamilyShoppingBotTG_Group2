import datetime as dt
from typing import Annotated, Optional
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from familybot.db.database import Base, session_factory


intpk = Annotated[int, mapped_column(primary_key=True)]
dtnow = Annotated[dt.datetime, mapped_column(server_default=func.now())]


class Family(Base):
    __tablename__ = 'families'
    id: Mapped[intpk]

    name: Mapped[str]
    members: Mapped[list["Person"]] = relationship(back_populates="family", lazy='joined')

    def __repr__(self):
        return f'<Family> {self.name}: {self.members}'

    def get_list(self):
        purchases = []

        for member in self.members:
            purchases += member.added_purchases

        return purchases

    def clean_purchases(self):
        for member in self.members:
            member.clean_purchases()


class Person(Base):
    __tablename__ = 'persons'
    id: Mapped[intpk]

    telegram_id: Mapped[str] = mapped_column(index=True, unique=True)
    name: Mapped[str]

    family_id: Mapped[int | None] = mapped_column(ForeignKey("families.id"))
    family: Mapped[Optional["Family"]] = relationship(back_populates="members", lazy='joined')
    is_owner: Mapped[bool | None] = None

    purchases: Mapped[list["Purchase"]] = relationship(back_populates="creator", lazy='joined')

    def __repr__(self):
        return f'<Person> {self.name} ({self.telegram_id})'
    
    def create_family(self, name: str | None = None) -> Family:  # self is host
        if name is None:
            name = f'Семья {self.name}'

        family = Family(name=name, members=[self])

        with session_factory() as session:
            session.add(family)
            session.commit()

        return family

    def clean_purchases(self):
        self.purchases[:] = []


class Purchase(Base):
    __tablename__ = 'purchases'
    id: Mapped[intpk]

    text: Mapped[str]

    is_done: Mapped[bool] = False
    creator_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    creator: Mapped["Person"] = relationship(back_populates="purchases", lazy='joined')
    created_at: Mapped[dtnow]

    deadline: Mapped[dt.datetime | None] = None

    def __repr__(self):
        return f'<Purchase> ({self.text}, {self.creator})'
