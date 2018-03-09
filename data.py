from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Model, User

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

print "USER ADDED!!!"

Mazda = Brand(
    user_id=1,
    name="Mazda"
    )
session.add(Mazda)
session.commit()

print "BRAND ADDED!!!!!!!!!!"

model1 = Model(
    user_id=1,
    name="3",
    description="FWD compact car with two engines to choose from ranging " +
    "from 155 to 184 hp",
    price="$17,845",
    category="sedan or hatchback",
    brand=Mazda
    )
session.add(model1)
session.commit()

# model2 = Model(
#     name="6",
#     description="FWD mid-size car with two engines to choose from ranging from 155 to 184 hp",
#     price="$21,945",
#     category="sedan",
#     brand=Mazda
#     )

print "car data added!"
