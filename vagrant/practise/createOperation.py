from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()
myFirstRestaurant = Restaurant(name='Luke Burger')
session.add(myFirstRestaurant)
session.commit()

session = DBSession()
cheesepizza = MenuItem(name='Cheese Pizza', description='Made with all natural ingredients and fresh Mozzarella',
                       course='Entree', price='$8.99', restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
