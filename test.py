from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Brand, Model

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

carMakers = session.query(Brand).all()
# selectedBrand = session.query(Brand).filter_by(id=brand_id).one()
# models = session.query(Model).filter_by(model_id=brand_id).all()
print carMakers
