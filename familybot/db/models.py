import enum
from sqlalchemy import func, ForeignKey, String, Integer, Boolean, Float, Column, Enum, DateTime
from sqlalchemy.orm import relationship
from familybot.db.database import Base


class Measurement(enum.Enum):
    count = 0
    weight = 1
    volume = 2


class Family(Base):
    __tablename__ = 'families'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    members = relationship('Person', backref='family', lazy='dynamic')


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)

    telegram_tag = Column(String)
    name = Column(String)

    family_id = Column(Integer, ForeignKey('families.id'), nullable=True)
    is_owner = Column(Boolean, default=False, nullable=True)

    added_purchases = relationship('Purchase', backref='creator', lazy='dynamic')

    def __str__(self):
        return f'{self.name} @{self.telegram_tag}'


class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)

    product_name = Column(String)
    amount = Column(Float)  # Maybe all nullable, except name?
    #  measurement = Column(Enum(Measurement))
    unit_price = Column(Float)

    is_done = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey('persons.id'))
    created_at = Column(DateTime, server_default=func.now())

    deadline = Column(DateTime, nullable=True)
