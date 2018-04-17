from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

UrbanVeggieBurger = session.query(MenuItem).filter_by(id= 9).one()

print("Price Before Update : " + UrbanVeggieBurger.price)

UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

print("Price After Update : " + UrbanVeggieBurger.price)

#Updating price of all the veggie burger
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

for veggieBurger in veggieBurgers:
    veggieBurger.price = '$2.99'
    session.add(veggieBurger)
    session.commit()
