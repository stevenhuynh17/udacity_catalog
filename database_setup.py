import os
import sys
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String(250))
    model_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship(Brand)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category': self.category,
            'brand': self.brand.name
        }


engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)

print "Database setup complete!"
