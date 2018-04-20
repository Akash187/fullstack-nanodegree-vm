from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
# database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API endpoint (get request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem= item.serialize)

#Making an API endpoint (get request)
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            newItem = MenuItem(name= request.form['name'], restaurant_id = restaurant_id)
            session.add(newItem)
            session.commit()
            flash('You were successfully added a new Item.')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    menuItem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        if request.form['newName']:
            newName= request.form['newName']
            menuItem.name = newName
            session.commit()
            flash('You were successfully edited an item.')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menuitem = menuItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menuitem_id):
    menuItem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash('You were successfully deleted an item.')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menuitem=menuItem)

if __name__ == '__main__':
    app.secret_key = 'W\xe1\x88+\xafD\xff\xde\xf3\x03\x04?\xf8\x8dz \xcd\xea5\xaa\xdf\xf4\xcbZ'
    app.debug = True
    app.run(host = '127.0.0.1', port = 5001)