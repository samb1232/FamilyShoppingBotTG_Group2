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
        return f'{self.name}: {self.members}'

    def get_list(self):
        purchases = []

        for member in self.members:
            purchases += member.added_purchases

        return purchases


class Person(Base):
    __tablename__ = 'persons'
    id: Mapped[intpk]

    telegram_tag: Mapped[str] = mapped_column(index=True, unique=True)
    name: Mapped[str]

    family_id: Mapped[int | None] = mapped_column(ForeignKey("families.id"))
    family: Mapped[Optional["Family"]] = relationship(back_populates="members")
    is_owner: Mapped[bool | None] = None

    purchases: Mapped[list["Purchase"]] = relationship(back_populates="creator", lazy='joined')

    def __repr__(self):
        return f'{self.name} @{self.telegram_tag}'
    
    def create_family(self, name: str | None = None) -> Family:  # self is host
        if name is None:
            name = f'Семья {self.name}'

        family = Family(name=name, members=[self])

        with session_factory() as session:
            session.add(family)
            session.commit()

        return family


class Purchase(Base):
    __tablename__ = 'purchases'
    id: Mapped[intpk]

    product_name: Mapped[str]
    amount: Mapped[float | None] = None
    #  measurement: Mapped[Enum(Measurement)]
    unit_price: Mapped[float | None] = None

    is_done: Mapped[bool] = False
    creator_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    creator: Mapped["Person"] = relationship(back_populates="purchases")
    created_at: Mapped[dtnow]

    deadline: Mapped[dt.datetime | None] = None

    def __repr__(self):
        return f'{self.product_name}'
