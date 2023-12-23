from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import and_
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:NewPassword@localhost:3306/dbinformationmanagement'
app.secret_key = 'dabeondona'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Furniture(db.Model):
    furniture_id = db.Column(db.Integer, primary_key=True)
    furniture_name = db.Column(db.String(200), nullable=False)
    furniture_quantity = db.Column(db.Integer, default=0)
    furniture_type = db.Column(db.String(100))
    furniture_weight = db.Column(db.Float)
    furniture_price = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    
    def update_availability(self):
        self.is_available = self.furniture_quantity > 0

    @property
    def id(self):
        return self.furniture_id
    
    
    
class Shoes(db.Model):
    shoes_id = db.Column(db.Integer, primary_key=True)
    shoes_name = db.Column(db.String(200), nullable=False)
    shoes_quantity = db.Column(db.Integer, default=0)
    shoes_brand = db.Column(db.String(100))
    shoes_size = db.Column(db.Integer)
    shoes_gender = db.Column(db.String(50))
    shoes_color = db.Column(db.String(50))
    shoes_price = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    
    def update_availability(self):
        self.is_available = self.shoes_quantity > 0

    @property
    def id(self):
        return self.shoes_id
    
class Appliances(db.Model):
    appliance_id = db.Column(db.Integer, primary_key=True)
    appliance_name = db.Column(db.String(200), nullable=False)
    appliance_quantity = db.Column(db.Integer, default=0)
    appliance_type = db.Column(db.String(100))
    appliance_brand = db.Column(db.String(100))
    appliance_weight = db.Column(db.Float)
    appliance_voltage = db.Column(db.Integer)
    appliance_price = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    
    def update_availability(self):
        self.is_available = self.appliance_quantity> 0
    
    @property
    def id(self):
        return self.appliance_id

class Stationery(db.Model):
    stationery_id = db.Column(db.Integer, primary_key=True)
    stationery_name = db.Column(db.String(200), nullable=False)
    stationery_brand = db.Column(db.String(100))
    stationery_type = db.Column(db.String(100))
    stationery_quantity = db.Column(db.Integer, default=0)
    stationery_price = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    
    def update_availability(self):
        self.is_available = self.stationery_quantity > 0

    @property
    def id(self):
        return self.stationery_id
    
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable = False)
    user_items_bought = db.Column(db.Integer)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    category = db.Column(db.String(100)) 
    item_id = db.Column(db.Integer) 

    def __repr__(self):
        return f'<Purchase {self.id}>'
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        user = User.query.filter_by(user_name=username).first()
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user.user_id 
            return redirect(url_for('store'))
        else:
            return 'User does not exist. Please check your username.'

    return render_template('login.html')

@app.route('/store')
def store():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    username = session.get('username', 'Guest') 
    user_id = session.get('user_id')
    
    furniture_items = Furniture.query.filter_by(is_available=True).all()
    shoes_items = Shoes.query.filter_by(is_available=True).all()
    appliances_items = Appliances.query.filter_by(is_available=True).all()
    stationery_items = Stationery.query.filter_by(is_available=True).all()

    return render_template('store.html', username=username, user_id=user_id, furniture_items=furniture_items, shoes_items=shoes_items, appliances_items=appliances_items, stationery_items=stationery_items)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user_name']

        existing_user = User.query.filter_by(user_name=username).first()
        if existing_user:
            return 'Username already exists. Please choose a different one.'

        new_user = User(user_name=username, user_items_bought=0)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f'An error occurred during registration: {e}'

    return render_template('create_user.html')

    
@app.route('/admin-dashboard')
def index():
    result = db.session.execute(text('SELECT * FROM category_summary'))
    categories = [{'category': row[0], 'count': row[1]} for row in result]
    categories.sort(key=lambda x: x['count'], reverse=True)
    users = User.query.all()
    return render_template('index.html', categories=categories, users=users)

@app.route('/user-purchases/<int:user_id>')
def user_purchases(user_id):
    
    purchases = db.session.query(
        Purchase.category,
        Purchase.item_id,
        Furniture.furniture_name,
        Furniture.furniture_price,
        Shoes.shoes_name,
        Shoes.shoes_price,
        Appliances.appliance_name,
        Appliances.appliance_price,
        Stationery.stationery_name,
        Stationery.stationery_price
    ).outerjoin(Furniture, and_(Purchase.category == 'Furniture', Purchase.item_id == Furniture.furniture_id)
    ).outerjoin(Shoes, and_(Purchase.category == 'Shoes', Purchase.item_id == Shoes.shoes_id)
    ).outerjoin(Appliances, and_(Purchase.category == 'Appliances', Purchase.item_id == Appliances.appliance_id)
    ).outerjoin(Stationery, and_(Purchase.category == 'Stationery', Purchase.item_id == Stationery.stationery_id)
    ).filter(Purchase.user_id == user_id).all()

    purchased_items = []
    for purchase in purchases:
        item_name = None
        item_price = None
        
        if purchase.category == 'Furniture' and purchase.furniture_name:
            item_name = purchase.furniture_name
            item_price = purchase.furniture_price
        elif purchase.category == 'Shoes' and purchase.shoes_name:
            item_name = purchase.shoes_name
            item_price = purchase.shoes_price
        elif purchase.category == 'Appliances' and purchase.appliance_name:
            item_name = purchase.appliance_name
            item_price = purchase.appliance_price
        elif purchase.category == 'Stationery' and purchase.stationery_name:
            item_name = purchase.stationery_name
            item_price = purchase.stationery_price
        
        formatted_price = "₱ {:.2f}".format(item_price) if item_price is not None else 'N/A'

        purchased_items.append({
            'category': purchase.category,
            'item_name': item_name if item_name else 'Item no longer available',
            'item_price': formatted_price
        })
        
    return render_template('user_purchases.html', purchases=purchased_items)

@app.route('/furniture', methods=['POST', 'GET'])
def furniture():
    if request.method == 'POST':
        furniture_name = request.form.get('furniture_name')
        furniture_type = request.form.get('furniture_type')
        furniture_quantity = int(request.form.get('furniture_quantity'))
        furniture_weight = float(request.form.get('furniture_weight'))
        furniture_price = float(request.form.get('furniture_price'))
        
        if furniture_name and furniture_type and furniture_quantity and furniture_weight and furniture_price:
            try:
                new_furniture = Furniture(
                    furniture_name=furniture_name,
                    furniture_type=furniture_type,
                    furniture_quantity=furniture_quantity,
                    furniture_weight=furniture_weight,
                    furniture_price=furniture_price
                )
                db.session.add(new_furniture)
                db.session.commit()
                return redirect('/furniture')
            except Exception as e:
                return f'An error occurred when adding the furniture: {e}'
    
    furniture_items = Furniture.query.all()
    return render_template('furniture.html', furniture_items=furniture_items)
    
    
@app.route('/shoes', methods=['POST', 'GET'])
def shoes():
    if request.method == 'POST':
        shoes_name = request.form.get('shoes_name')
        shoes_quantity = int(request.form.get('shoes_quantity'))
        shoes_brand = request.form.get('shoes_brand')
        shoes_size = int(request.form.get('shoes_size'))
        shoes_gender = request.form.get('shoes_gender')
        shoes_color = request.form.get('shoes_color')
        shoes_price = float(request.form.get('shoes_price'))
        
        if shoes_name and shoes_quantity and shoes_brand and shoes_size and shoes_gender and shoes_color and shoes_price:
            try:
                new_shoes = Shoes(
                    shoes_name=shoes_name,
                    shoes_quantity=shoes_quantity,
                    shoes_brand=shoes_brand,
                    shoes_size=shoes_size,
                    shoes_gender=shoes_gender,
                    shoes_color=shoes_color,
                    shoes_price=shoes_price
                )
                db.session.add(new_shoes)
                db.session.commit()
                return redirect('/shoes')
            except Exception as e:
                return f'An error occurred when adding the shoes: {e}'
    
    shoes_items = Shoes.query.all()
    return render_template('shoes.html', shoes_items=shoes_items)

    
@app.route('/appliances', methods=['POST', 'GET'])
def appliances():
    if request.method == 'POST':
        appliance_name = request.form.get('appliance_name')
        appliance_quantity = int(request.form.get('appliance_quantity'))
        appliance_type = request.form.get('appliance_type')
        appliance_brand = request.form.get('appliance_brand')
        appliance_weight = float(request.form.get('appliance_weight'))
        appliance_voltage = int(request.form.get('appliance_voltage'))
        appliance_price = float(request.form.get('appliance_price'))
        
        if appliance_name and appliance_quantity and appliance_type and appliance_brand and appliance_weight and appliance_voltage and appliance_price:
            try:
                new_appliance = Appliances(
                    appliance_name=appliance_name,
                    appliance_quantity=appliance_quantity,
                    appliance_type=appliance_type,
                    appliance_brand=appliance_brand,
                    appliance_weight=float(appliance_weight),
                    appliance_voltage=int(appliance_voltage),
                    appliance_price=float(appliance_price)
                )
                db.session.add(new_appliance)
                db.session.commit()
                return redirect('/appliances')
            except Exception as e:
                return f'An error occurred when adding the appliance: {e}'
    
    appliances_items = Appliances.query.all()
    return render_template('appliances.html', appliances_items=appliances_items)

    
@app.route('/stationery', methods=['POST', 'GET'])
def stationery():
    if request.method == 'POST':
        stationery_name = request.form.get('stationery_name')
        stationery_brand = request.form.get('stationery_brand')
        stationery_type = request.form.get('stationery_type')
        stationery_quantity = int(request.form.get('stationery_quantity'))
        stationery_price = float(request.form.get('stationery_price'))
        
        if stationery_name and stationery_brand and stationery_type and stationery_quantity and stationery_price:
            try:
                new_stationery = Stationery(
                    stationery_name=stationery_name,
                    stationery_brand=stationery_brand,
                    stationery_type=stationery_type,
                    stationery_quantity=int(stationery_quantity),
                    stationery_price=float(stationery_price)
                )
                db.session.add(new_stationery)
                db.session.commit()
                return redirect('/stationery')
            except Exception as e:
                return f'An error occurred when adding the stationery: {e}'
    
    stationery_items = Stationery.query.all()
    return render_template('stationery.html', stationery_items=stationery_items)

    
def get_model_by_category(category):
    if category == 'furniture':
        return Furniture
    elif category == 'shoes':
        return Shoes
    elif category == 'appliances':
        return Appliances
    elif category == 'stationery':
        return Stationery
    else:
        return None

@app.route('/delete/<category>/<int:id>')
def delete(category, id):
    model = get_model_by_category(category)
    if model is None:
        return 'Invalid category'

    item_to_delete = model.query.get_or_404(id)
    
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/admin-dashboard')
    except:
        return 'There was a problem deleting that item'
    
@app.route('/update/furniture/<int:id>', methods=['GET', 'POST'])
def furnitureUpdate(id):
    furniture_item = Furniture.query.get_or_404(id)

    if request.method == 'POST':
        furniture_item.furniture_name = request.form.get('furniture_name')
        furniture_item.furniture_type = request.form.get('furniture_type')
        furniture_item.furniture_quantity = int(request.form.get('furniture_quantity', 0))
        furniture_item.furniture_weight = float(request.form.get('furniture_weight', 0))
        furniture_item.furniture_price = float(request.form.get('furniture_price', 0))
        furniture_item.update_availability()

        try:
            db.session.commit()
            return redirect('/furniture')
        except Exception as e:
            return f'There was an issue updating the furniture item: {e}'

    else:
        return render_template('furnitureupdate.html', item=furniture_item)
    
@app.route('/update/shoes/<int:id>', methods=['GET', 'POST'])
def shoesUpdate(id):
    shoes_item = Shoes.query.get_or_404(id)

    if request.method == 'POST':
        shoes_item.shoes_name = request.form.get('shoes_name')
        shoes_item.shoes_quantity = int(request.form.get('shoes_quantity', 0))
        shoes_item.shoes_brand = request.form.get('shoes_brand')
        shoes_item.shoes_size = int(request.form.get('shoes_size', 0))
        shoes_item.shoes_gender = request.form.get('shoes_gender')
        shoes_item.shoes_color = request.form.get('shoes_color')
        shoes_item.shoes_price = float(request.form.get('shoes_price', 0))
        shoes_item.update_availability()

        try:
            db.session.commit()
            return redirect('/shoes')
        except Exception as e:
            return f'There was an issue updating the shoes item: {e}'

    else:
        return render_template('shoesupdate.html', item=shoes_item)
    
@app.route('/update/appliances/<int:id>', methods=['GET', 'POST'])
def appliancesUpdate(id):
    appliance_item = Appliances.query.get_or_404(id)

    if request.method == 'POST':
        appliance_item.appliance_name = request.form.get('appliance_name')
        appliance_item.appliance_quantity = int(request.form.get('appliance_quantity', 0))
        appliance_item.appliance_type = request.form.get('appliance_type')
        appliance_item.appliance_brand = request.form.get('appliance_brand')
        appliance_item.appliance_weight = float(request.form.get('appliance_weight', 0))
        appliance_item.appliance_voltage = int(request.form.get('appliance_voltage', 0))
        appliance_item.appliance_price = float(request.form.get('appliance_price', 0))
        appliance_item.update_availability()

        try:
            db.session.commit()
            return redirect('/appliances')
        except Exception as e:
            return f'There was an issue updating the appliance item: {e}'

    else:
        return render_template('appliancesupdate.html', item=appliance_item)
    
@app.route('/update/stationery/<int:id>', methods=['GET', 'POST'])
def stationeryUpdate(id):
    stationery_item = Stationery.query.get_or_404(id)

    if request.method == 'POST':
        stationery_item.stationery_name = request.form.get('stationery_name')
        stationery_item.stationery_brand = request.form.get('stationery_brand')
        stationery_item.stationery_type = request.form.get('stationery_type')
        stationery_item.stationery_quantity = int(request.form.get('stationery_quantity', 0))
        stationery_item.stationery_price = float(request.form.get('stationery_price', 0))
        stationery_item.update_availability()

        try:
            db.session.commit()
            return redirect('/stationery')
        except Exception as e:
            return f'There was an igetattrssue updating the stationery item: {e}'

    else:
        return render_template('stationeryupdate.html', item=stationery_item)
    
@app.route('/buy/<category>/<int:item_id>')
def buy(category, item_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    if user_id is None:
        return 'You must be logged in to make a purchase.', 403

    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404

    model = get_model_by_category(category)
    if model is None:
        return 'Invalid category', 404

    item = model.query.get(item_id)
    if item is None:
        return 'Item not found', 404

    item_quantity_attribute = f'{category}_quantity'
    if getattr(item, item_quantity_attribute) > 0:
        setattr(item, item_quantity_attribute, getattr(item, item_quantity_attribute) - 1)
        item.update_availability()

        user.user_items_bought = user.user_items_bought + 1 if user.user_items_bought else 1

        db.session.add(Purchase(user_id=user_id, category=category.capitalize(), item_id=item_id))
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error(f'Error when saving purchase: {e}')
            db.session.rollback()
            return 'An error occurred while saving the purchase.', 500
        
        return redirect(url_for('store'))
    else:
        return 'This item is out of stock.'

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
    app.logger.debug(f'Current quantity of item {item_id} is {current_quantity}')
