from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask.ext.login import LoginManager
from database_setup import Restaurant, Base, MenuItem, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine

app = Flask(__name__)
# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Creating database session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db = DBSession()


# ------------------------ Login functionality ------------------------------ #
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid_username = db.query(User).filter(User.username.in_([username])).first()
        if valid_username:
            valid_password = db.query(User).filter(User.username.in_([username]),
                                                   User.password.in_([password])).first()
            if valid_password:
                session['logged_in'] = True
                flash('You are logged in')
                restaurants = db.query(Restaurant).all()
                return render_template('all_restaurants.html', restaurants=restaurants)
            else:
                error = 'Invalid password'
        else:
            error = 'User does not exist'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username_exists = db.query(User).filter(User.username.in_([username])).first()
        if username_exists:
            flash('Username not available')
            return redirect(url_for('register_user'))
        else:
            new_user = User(username=username, password=password)
            db.add(new_user)
            db.commit
            flash('User details created')
            return redirect(url_for('login'))
    else:
        return render_template('user_registration.html')


def get_auth_status():
    return session.get('logged_in')
# ------------------------------------------------------------------- #


# -------------------------- API Endpoints -------------------------- #
@app.route('/restaurants/asJSON')
def restaurants_as_json():
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        restaurants = db.query(Restaurant).all()
        return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menus/asJSON')
def restaurant_menu_as_json(restaurant_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        restaurant = db.query(Restaurant).filter_by(id=restaurant_id).one()
        items = db.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/asJSON')
def specific_restaurant_menu_as_json(restaurant_id,menu_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        restaurant = db.query(Restaurant).filter_by(id=restaurant_id).one()
        item = db.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant.id).one()
        return jsonify(MenuItem=item.serialize)
# ------------------------------------------------------------------- #


# ----------------------- Restaurant CRUD --------------------------- #
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/restaurants', methods=['GET'])
def get_all_restaurants():
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        try:
            restaurants = db.query(Restaurant).all()
            return render_template('all_restaurants.html', restaurants=restaurants)
        except NoResultFound:
            return render_template('no_restaurant.html', restaurant=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def add_new_restaurant():
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            new_restaurant = Restaurant(name=request.form['name'])
            db.add(new_restaurant)
            db.commit()
            flash("New restaurant is created")
            return redirect(url_for('get_all_restaurants'))
        else:
            return render_template('new_restaurant.html')


@app.route('/restaurants/<restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        restaurant_to_edit = db.query(Restaurant).filter_by(id=restaurant_id).one()
        if request.method == 'POST':
            restaurant_to_edit.name = request.form['name']
            restaurant_to_edit.description = request.form['description']
            restaurant_to_edit.price = request.form['price']
            restaurant_to_edit.course = request.form['course']
            db.add(restaurant_to_edit)
            db.commit()
            flash("Restaurant details are edited")
            return redirect(url_for('get_all_restaurants'))
        else:
            return render_template('edit_restaurant.html', id=restaurant_id,
                                   i=restaurant_to_edit)


@app.route('/restaurants/<restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        restaurant_to_delete = db.query(Restaurant).filter_by(id=restaurant_id).one()
        if request.method == 'POST':
            db.delete(restaurant_to_delete)
            db.commit()
            flash("Restaurant is deleted")
            return redirect(url_for('get_all_restaurants'))
        else:
            return render_template('delete_restaurant.html', id=restaurant_id,
                                   i=restaurant_to_delete)
# ------------------------------------------------------------------------------------- #


# -------------------------------- Menu Item CRUD ------------------------------------- #
@app.route('/restaurant/<int:restaurant_id>/menus', methods=['GET'])
def restaurant_menu(restaurant_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        restaurant = db.query(Restaurant).filter_by(id=restaurant_id).one()
        items = db.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        if items.count() != 0:
            return render_template('restaurant_menu.html', restaurant=restaurant, items=items)
        else:
            return render_template('no_menuitem.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def create_menu_item(restaurant_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            new_menu_item = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'],
                                     restaurant_id=restaurant_id)
            db.add(new_menu_item)
            db.commit()
            flash("New menu item is created")
            return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
        else:
            return render_template('new_menuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        item_to_edit = db.query(MenuItem).filter_by(id=menu_id).one()
        if request.method == 'POST':
            item_to_edit.name = request.form['name']
            item_to_edit.description = request.form['description']
            item_to_edit.price = request.form['price']
            item_to_edit.course = request.form['course']
            db.add(item_to_edit)
            db.commit()
            flash("Requested menu item is edited")
            return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
        else:
            return render_template('edit_menuitem.html', restaurant_id=restaurant_id,
                                   menu_id=menu_id, i=item_to_edit)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    auth_status = get_auth_status()
    if auth_status is None:
        return redirect(url_for('index'))
    else:
        item_to_delete = db.query(MenuItem).filter_by(id=menu_id).one()
        if request.method == 'POST':
            db.delete(item_to_delete)
            db.commit()
            flash("Menu item is deleted")
            return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
        else:
            return render_template('delete_menuitem.html', restaurant_id=restaurant_id,
                                   menu_id=menu_id, i=item_to_delete)
# ----------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    app.secret_key = 'password'
    app.run(debug=True, host='0.0.0.0', port=5000)
