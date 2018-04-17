from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

spinch = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
session.delete(spinch)
session.commit()