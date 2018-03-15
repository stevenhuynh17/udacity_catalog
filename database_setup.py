import os
import sys
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String(250))

    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship(Brand, backref=backref("brand", cascade="all, delete-orphan"))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'brand': self.brand.name,
            'user': self.user.name
        }


engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)

print "Database setup complete!"
