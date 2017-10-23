from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Model

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

Mazda = Brand(name="Mazda")
session.add(Mazda)
session.commit()

model1 = Model(
    name="3",
    description="FWD compact car with two engines to choose from ranging from 155 to 184 hp",
    price="$17,845",
    category="sedan or hatchback",
    brand=Mazda
    )
session.add(model1)
session.commit()

model2 = Model(
    name="6",
    description="FWD mid-size car with two engines to choose from ranging from 155 to 184 hp",
    price="$21,945",
    category="sedan",
    brand=Mazda
    )
session.add(model2)
session.commit()

Tesla = Brand(name="Tesla")
session.add(Tesla)

model1 = Model(
    name="S",
    description="RWD or AWD full size luxury car with various motors that put out 382 to 691 hp",
    price="$68,000",
    category="sedan",
    brand=Tesla
)

session.add(model1)
session.commit()

print "car data added!"
