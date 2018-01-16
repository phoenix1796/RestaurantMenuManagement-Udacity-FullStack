'''
Just another docstring
'''
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()

    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def specificMenuItemJSON(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one() # To check against arbitrary inputs to the API
    item = session.query(MenuItem).filter_by(id = menu_id,restaurant_id=restaurant_id).one()
    return jsonify(MenuItem=item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html',restaurant_id = restaurant_id)
    # return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu item edited.")
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html',restaurant_id = restaurant_id,menu_id = menu_id, item = editedItem)
     # return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete", methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item deleted.")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',item=itemToDelete)
    # return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
