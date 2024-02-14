import datetime as dt
from typing import Annotated
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from familybot.db.database import Base, session_factory


intpk = Annotated[int, mapped_column(primary_key=True)]
dtnow = Annotated[dt.datetime, mapped_column(server_default=func.now())]


class Family(Base):
    __tablename__ = 'families'
    id: Mapped[intpk]

    name: Mapped[str]
    members: Mapped[list["Person"]] = relationship(backref='family', cascade='all, delete-orphan', lazy='noload')

    def __repr__(self):
        return f'{self.name}: {" ".join(map(str, self.members))}'

    def get_list(self):
        purchases = []

        for member in self.members:
            purchases += member.added_purchases

        return purchases


class Person(Base):
    __tablename__ = 'persons'
    id: Mapped[intpk]

    telegram_tag: Mapped[str]
    name: Mapped[str]

    family_id: Mapped["Family"] = mapped_column(ForeignKey("families.id"), nullable=True)
    is_owner: Mapped[bool | None] = None

    added_purchases: Mapped[list["Purchase"]] = relationship(backref='creator', cascade='all, delete-orphan', lazy='noload')

    def __repr__(self):
        return f'{self.name} @{self.telegram_tag}'

    def add_purchase(self, purchase: "Purchase") -> None:
        with session_factory() as session:
            self.added_purchases.append(purchase)
            session.commit()


class Purchase(Base):
    __tablename__ = 'purchases'
    id: Mapped[intpk]

    product_name: Mapped[str]
    amount: Mapped[float | None] = None
    #  measurement = Column(Enum(Measurement))
    unit_price: Mapped[float | None] = None

    is_done: Mapped[bool] = False
    creator_id: Mapped["Person"] = mapped_column(ForeignKey("persons.id"))
    created_at: Mapped[dtnow]

    deadline: Mapped[dt.datetime | None] = None

    def __repr__(self):
        return f'{self.product_name}'
