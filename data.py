from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Model, User

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

# User Data
User1 = User(
    name="Robo Barista",
    email="tinnyTim@udacity.com",
    picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)
session.add(User1)
session.commit()
print "USERS ADDED!!!"

Mazda = Brand(
    name="Mazda",
    user=User1
)
session.add(Mazda)
session.commit()

Mazda3 = Model(
    name="Mazda3",
    description="Entry level car",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Mazda
)
session.add(Mazda3)
session.commit()

Tesla = Brand(
    name="Tesla",
    user=User1)
session.add(Tesla)
session.commit()

Model3 = Model(
    name="Model S",
    description="Full size luxury electric car",
    price="$60,000",
    category="sedan",
    user=User1,
    brand=Tesla
)
session.add(Model3)
session.commit()

print "Brands and models added!"
