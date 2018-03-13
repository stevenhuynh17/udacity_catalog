from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Brand, Model

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

# print session.query(User).one().id
print session.query(Model).first().brand.name
