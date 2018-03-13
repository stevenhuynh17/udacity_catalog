from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Brand, Model

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

# carMakers = session.query(Brand).all()
selectedBrand = session.query(Brand).filter_by(name="Mazda").one()
print selectedBrand.id
models = session.query(Model).filter_by(brand_id=1).all()[0].name
print models

# for brand in carMakers:
#     print brand.name
