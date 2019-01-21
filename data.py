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
print ("USERS ADDED!!!")

Lexus = Brand(
    name="Lexus",
    user=User1,
    img="../../static/img/logo/lexus.svg"
)
session.add(Lexus)
session.commit()

RCF = Model(
    name="RCF",
    img="../../static/img/lexus_rcf_2015.jpg",
    description="Japanese luxury performance sports coupe",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Lexus
)
session.add(RCF)
session.commit()

Mazda = Brand(
    name="Mazda",
    user=User1,
    img="../../static/img/logo/mazda.svg"
)
session.add(Mazda)
session.commit()

Mazda3 = Model(
    name="Mazda3",
    img="../../static/img/mazda3_2017.jpg",
    description="Japanese compact entry level car in sedan or hatchback",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Mazda
)
session.add(Mazda3)
session.commit()

Tesla = Brand(
    name="Tesla",
    user=User1,
    img="../../static/img/logo/tesla.svg"
)
session.add(Tesla)
session.commit()

Model3 = Model(
    name="Model S",
    img="../../static/img/tesla_modelS_2017.jpg",
    description="American built, full size luxury electric car",
    price="$60,000",
    category="sedan",
    user=User1,
    brand=Tesla
)
session.add(Model3)
session.commit()

Acura = Brand(
    name="Acura",
    user=User1,
    img="../../static/img/logo/acura.svg"
)
session.add(Acura)
session.commit()

NSX = Model(
    name="NSX",
    img="../../static/img/acura_nsx_2018.jpg",
    description="Japanese supercar in coupe",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Acura
)
session.add(NSX)
session.commit()

Audi = Brand(
    name="Audi",
    user=User1,
    img="../../static/img/logo/audi.svg"
)
session.add(Audi)
session.commit()

R8 = Model(
    name="R8",
    img="../../static/img/audi_r8_2018.jpg",
    description="German supercar in coupe or convertible",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Audi
)
session.add(R8)
session.commit()

BMW = Brand(
    name="BMW",
    user=User1,
    img="../../static/img/logo/bmw.svg"
)
session.add(BMW)
session.commit()

M4 = Model(
    name="M4",
    img="../../static/img/bmw_m4_2018.jpg",
    description="German high performance luxury sports coupe",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=BMW
)
session.add(M4)
session.commit()

Honda = Brand(
    name="Honda",
    user=User1,
    img="../../static/img/logo/honda.svg"
)
session.add(Honda)
session.commit()

TypeR = Model(
    name="TypeR",
    img="../../static/img/honda_civicR_2018.jpg",
    description="Japanese mid level high performance sedan",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Honda
)
session.add(TypeR)
session.commit()

Infiniti = Brand(
    name="Infiniti",
    user=User1,
    img="../../static/img/logo/infiniti.svg"
)
session.add(Infiniti)
session.commit()

Q60 = Model(
    name="Q60",
    img="../../static/img/infiniti_q60_2019.jpg",
    description="Japanese mid level premium sports coupe",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Mazda
)
session.add(Q60)
session.commit()

Nissan = Brand(
    name="Nissan",
    user=User1,
    img="../../static/img/logo/nissan.svg"
)
session.add(Nissan)
session.commit()

GTR = Model(
    name="GTR",
    img="../../static/img/nissan_gtr_2017.jpg",
    description="Japanese high performance sports coupe",
    price="$20,000",
    category="sedan",
    user=User1,
    brand=Nissan
)
session.add(Mazda3)
session.commit()


print ("Brands and models added!")
