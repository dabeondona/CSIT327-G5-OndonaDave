from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import and_
from sqlalchemy.sql import text
from sqlalchemy import inspect  
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/dbinformationmanagement'
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



# Create Furniture
def create_furniture(name, furniture_type, weight, price):
    try:
        new_furniture = Furniture(
            furniture_name=name,
            furniture_type=furniture_type,
            furniture_weight=weight,
            furniture_price=price
        )
        db.session.add(new_furniture)
        db.session.commit()

        # Log the creation action
        log_furniture_action(new_furniture.furniture_id, 'CREATE')
        return True
    except Exception as e:
        print(f'Error creating furniture: {e}')
        db.session.rollback()
        return False

# Read Furniture
def get_all_furniture():
    return Furniture.query.all()

def get_furniture_by_id(furniture_id):
    return Furniture.query.get(furniture_id)

# Update Furniture
def update_furniture_price(furniture_id, new_price):
    try:
        furniture = Furniture.query.get(furniture_id)
        if furniture:
            old_price = furniture.furniture_price
            furniture.furniture_price = new_price
            db.session.commit()

            # Log the update action
            log_furniture_price_update(furniture_id, old_price, new_price)
            return True
        else:
            return False
    except Exception as e:
        print(f'Error updating furniture price: {e}')
        db.session.rollback()
        return False

# Delete Furniture
def delete_furniture(furniture_id):
    try:
        furniture = Furniture.query.get(furniture_id)
        if furniture:
            db.session.delete(furniture)
            db.session.commit()

            # Log the deletion action
            log_furniture_action(furniture_id, 'DELETE')
            return True
        else:
            return False
    except Exception as e:
        print(f'Error deleting furniture: {e}')
        db.session.rollback()
        return False

# Audit Logging Functions for Furniture
def log_furniture_action(furniture_id, action):
    try:
        new_audit_log = FurnitureAudit(
            furniture_id=furniture_id,
            action=action,
            timestamp=datetime.now()
        )
        db.session.add(new_audit_log)
        db.session.commit()
    except Exception as e:
        print(f'Error logging furniture action: {e}')
        db.session.rollback()

def log_furniture_price_update(furniture_id, old_price, new_price):
    try:
        action_details = f'Price updated from {old_price} to {new_price}'
        new_audit_log = FurnitureAudit(
            furniture_id=furniture_id,
            action=action_details,
            timestamp=datetime.now()
        )
        db.session.add(new_audit_log)
        db.session.commit()
    except Exception as e:
        print(f'Error logging furniture price update: {e}')
        db.session.rollback()


# Create Shoes
def create_shoes(name, brand, size, gender, color, price):
    try:
        new_shoes = Shoes(
            shoes_name=name,
            shoes_brand=brand,
            shoes_size=size,
            shoes_gender=gender,
            shoes_color=color,
            shoes_price=price
        )
        db.session.add(new_shoes)
        db.session.commit()

        # Log the creation action
        log_shoes_action(new_shoes.shoes_id, 'CREATE')
        return True
    except Exception as e:
        print(f'Error creating shoes: {e}')
        db.session.rollback()
        return False

# Read Shoes
def get_all_shoes():
    return Shoes.query.all()

def get_shoes_by_id(shoes_id):
    return Shoes.query.get(shoes_id)

# Update Shoes
def update_shoes_price(shoes_id, new_price):
    try:
        shoes = Shoes.query.get(shoes_id)
        if shoes:
            old_price = shoes.shoes_price
            shoes.shoes_price = new_price
            db.session.commit()

            # Log the update action
            log_shoes_price_update(shoes_id, old_price, new_price)
            return True
        else:
            return False
    except Exception as e:
        print(f'Error updating shoes price: {e}')
        db.session.rollback()
        return False

# Delete Shoes
def delete_shoes(shoes_id):
    try:
        shoes = Shoes.query.get(shoes_id)
        if shoes:
            db.session.delete(shoes)
            db.session.commit()

            # Log the deletion action
            log_shoes_action(shoes_id, 'DELETE')
            return True
        else:
            return False
    except Exception as e:
        print(f'Error deleting shoes: {e}')
        db.session.rollback()
        return False

# Audit Logging Functions for Shoes
def log_shoes_action(shoes_id, action):
    try:
        new_audit_log = ShoesAudit(
            shoes_id=shoes_id,
            action=action,
            timestamp=datetime.now()
        )
        db.session.add(new_audit_log)
        db.session.commit()
    except Exception as e:
        print(f'Error logging shoes action: {e}')
        db.session.rollback()

def log_shoes_price_update(shoes_id, old_price, new_price):
    try:
        action_details = f'Price updated from {old_price} to {new_price}'
        new_audit_log = ShoesAudit(
            shoes_id=shoes_id,
            action=action_details,
            timestamp=datetime.now()
        )
        db.session.add(new_audit_log)
        db.session.commit()
    except Exception as e:
        print(f'Error logging shoes price update: {e}')
        db.session.rollback()


# Create Appliances
def create_appliance(name, appliance_type, brand, weight, voltage, price):
    try:
        new_appliance = Appliances(
            appliance_name=name,
            appliance_type=appliance_type,
            appliance_brand=brand,
            appliance_weight=weight,
            appliance_voltage=voltage,
            appliance_price=price
        )
        db.session.add(new_appliance)
        db.session.commit()

        # Log the creation action
        log_appliance_action(new_appliance.appliance_id, 'CREATE')
        return True
    except Exception as e:
        print(f'Error creating appliance: {e}')
        db.session.rollback()
        return False

# Read Appliances
def get_all_appliances():
    return Appliances.query.all()

def get_appliance_by_id(appliance_id):
    return Appliances.query.get(appliance_id)

# Update Appliances
def update_appliance_price(appliance_id, new_price):
    try:
        appliance = Appliances.query.get(appliance_id)
        if appliance:
            old_price = appliance.appliance_price
            appliance.appliance_price = new_price
            db.session.commit()

            # Log the update action
            log_appliance_price_update(appliance_id, old_price, new_price)
            return True
        else:
            return False
    except Exception as e:
        print(f'Error updating appliance price: {e}')
        db.session.rollback()
        return False

# Delete Appliances
def delete_appliance(appliance_id):
    try:
        appliance = Appliances.query.get(appliance_id)
        if appliance:
            db.session.delete(appliance)
            db.session.commit()

            # Log the deletion action
            log_appliance_action(appliance_id, 'DELETE')
            return True
        else:
            return False
    except Exception as e:
        print(f'Error deleting appliance: {e}')
        db.session.rollback()
        return False

# Audit Logging Functions for Appliances
def log_appliance_action(appliance_id, action):
    try:
        new_audit_log = AppliancesAudit(
            appliance_id=appliance_id,
            action=action,
            timestamp=datetime.now()
        )
        db.session.add(new_audit_log)
        db.session.commit()
    except Exception as e:
        print(f'Error logging appliance action: {e}')
        db.session.rollback()

def log_appliance_price_update(appliance_id, old_price, new_price):
    try:
        action_details = f'Price updated from {old_price} to {new_price}'
        new_audit_log = AppliancesAudit(
            appliance_id=appliance_id,
            action=action_details,
            timestamp=datetime.now()
        )
        db.session.add(new_audit_log)
        db.session.commit()
    except Exception as e:
        print(f'Error logging appliance price update: {e}')
        db.session.rollback()


# Create Stationery
def create_stationery(name, brand, stationery_type, quantity, price):
    try:
        new_stationery = Stationery(
            stationery_name=name,
            stationery_brand=brand,
            stationery_type=stationery_type,
            stationery_quantity=quantity,
            stationery_price=price
        )
        db.session.add(new_stationery)
        db.session.commit()

        # Log the creation action
        log_stationery_action(new_stationery.stationery_id, 'CREATE')
        return True
    except Exception as e:
        print(f'Error creating stationery: {e}')
        db.session.rollback()
        return False

# Read Stationery
def get_all_stationery():
    return Stationery.query.all()

def get_stationery_by_id(stationery_id):
    return Stationery.query.get(stationery_id)

# Update Stationery
def update_stationery_price(stationery_id, new_price):
    try:
        stationery = Stationery.query.get(stationery_id)
        if stationery:
            old_price = stationery.stationery_price
            stationery.stationery_price = new_price
            db.session.commit()

            # Log the update action
            log_stationery_price_update(stationery_id, old_price, new_price)
            return True
        else:
            return False
    except Exception as e:
        print(f'Error updating stationery price: {e}')
        db.session.rollback()
        return False


# Delete Stationery
def delete_stationery(stationery_id):
    try:
        stationery = Stationery.query.get(stationery_id)
        if stationery:
            db.session.delete(stationery)
            db.session.commit()

            # Log the deletion action
            log_stationery_action(stationery_id, 'DELETE')
            return True
        else:
            return False
    except Exception as e:
        print(f'Error deleting stationery: {e}')
        db.session.rollback()
        return False




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

        inspector = inspect(db.engine)
        existing_views = inspector.get_view_names()

        if 'category_summary' not in existing_views:
            # SQL command to create the category_summary view
            create_view_query = '''
                CREATE 
                    ALGORITHM = UNDEFINED 
                    DEFINER = root@localhost
                    SQL SECURITY DEFINER
                VIEW `dbinformationmanagement`.`category_summary` AS
                    SELECT 
                        'Furniture' AS `category`, COUNT(0) AS `count`
                    FROM
                        `dbinformationmanagement`.`furniture` 
                    UNION ALL SELECT 
                        'Shoes' AS `Shoes`, COUNT(0) AS `COUNT(*)`
                    FROM
                        `dbinformationmanagement`.`shoes` 
                    UNION ALL SELECT 
                        'Appliances' AS `Appliances`, COUNT(0) AS `COUNT(*)`
                    FROM
                        `dbinformationmanagement`.`appliances` 
                    UNION ALL SELECT 
                        'Stationery' AS `Stationery`, COUNT(0) AS `COUNT(*)`
                    FROM
                        `dbinformationmanagement`.`stationery`
                    ORDER BY `count` DESC;
            '''
            db.session.execute(text(create_view_query))
            db.session.commit()


        

# Stored procedures
with app.app_context():
    try:
        db.create_all()

        # Check if InsertFurniture procedure exists before creating it
        result = db.session.execute(text("SHOW PROCEDURE STATUS WHERE Db = 'dbinformationmanagement' AND Name = 'InsertFurniture'"))
        procedure_exists = result.rowcount > 0

        if not procedure_exists:
            # Stored procedure: InsertFurniture
            db.session.execute(text('''
                CREATE PROCEDURE InsertFurniture(
                    IN furniture_name VARCHAR(200),
                    IN furniture_type VARCHAR(100),
                    IN furniture_weight FLOAT,
                    IN furniture_price FLOAT
                )
                BEGIN
                    INSERT INTO Furniture (furniture_name, furniture_type, furniture_weight, furniture_price)
                    VALUES (furniture_name, furniture_type, furniture_weight, furniture_price);
                END;
            '''))
            db.session.commit()

            

    except Exception as e:
        print(f"Error creating stored procedures: {e}")

        # Stored procedure: UpdateFurniturePrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateFurniturePrice(
                IN p_furniture_id INT,
                IN p_new_price FLOAT
            )
            BEGIN
                UPDATE Furniture
                SET furniture_price = p_new_price
                WHERE furniture_id = p_furniture_id;
            END;
        '''))

        # Stored procedure: DeleteFurnitureById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteFurnitureById(
                IN p_furniture_id INT
            )
            BEGIN
                DELETE FROM Furniture
                WHERE furniture_id = p_furniture_id;
            END;
        '''))

        # Stored procedure: InsertShoes
        db.session.execute(text('''
            CREATE PROCEDURE InsertShoes(
                IN shoes_name VARCHAR(200),
                IN shoes_brand VARCHAR(100),
                IN shoes_size INT,
                IN shoes_gender VARCHAR(50),
                IN shoes_color VARCHAR(50),
                IN shoes_price FLOAT
            )
            BEGIN
                INSERT INTO Shoes (shoes_name, shoes_brand, shoes_size, shoes_gender, shoes_color, shoes_price)
                VALUES (shoes_name, shoes_brand, shoes_size, shoes_gender, shoes_color, shoes_price);
            END;
        '''))

        # Stored procedure: UpdateShoesPrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateShoesPrice(
                IN shoes_id INT,
                IN new_price FLOAT
            )
            BEGIN
                UPDATE Shoes
                SET shoes_price = new_price
                WHERE shoes_id = shoes_id;
            END;
        '''))

        # Stored procedure: DeleteShoesById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteShoesById(
                IN shoes_id INT
            )
            BEGIN
                DELETE FROM Shoes
                WHERE shoes_id = shoes_id;
            END;
        '''))

        # Stored procedure: InsertAppliance
        db.session.execute(text('''
            CREATE PROCEDURE InsertAppliance(
                IN appliance_name VARCHAR(200),
                IN appliance_type VARCHAR(100),
                IN appliance_brand VARCHAR(100),
                IN appliance_weight FLOAT,
                IN appliance_voltage INT,
                IN appliance_price FLOAT
            )
            BEGIN
                INSERT INTO Appliances (appliance_name, appliance_type, appliance_brand, appliance_weight, appliance_voltage, appliance_price)
                VALUES (appliance_name, appliance_type, appliance_brand, appliance_weight, appliance_voltage, appliance_price);
            END;
        '''))

        # Stored procedure: UpdateAppliancePrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateAppliancePrice(
                IN appliance_id INT,
                IN new_price FLOAT
            )
            BEGIN
                UPDATE Appliances
                SET appliance_price = new_price
                WHERE appliance_id = appliance_id;
            END;
        '''))

        # Stored procedure: DeleteApplianceById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteApplianceById(
                IN appliance_id INT
            )
            BEGIN
                DELETE FROM Appliances
                WHERE appliance_id = appliance_id;
            END;
        '''))

        # Stored procedure: InsertStationery
        db.session.execute(text('''
            CREATE PROCEDURE InsertStationery(
                IN stationery_name VARCHAR(200),
                IN stationery_brand VARCHAR(100),
                IN stationery_type VARCHAR(100),
                IN stationery_quantity INT,
                IN stationery_price FLOAT
            )
            BEGIN
                INSERT INTO Stationery (stationery_name, stationery_brand, stationery_type, stationery_quantity, stationery_price)
                VALUES (stationery_name, stationery_brand, stationery_type, stationery_quantity, stationery_price);
            END;
        '''))

        # Stored procedure: UpdateStationeryPrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateStationeryPrice(
                IN stationery_id INT,
                IN new_price FLOAT
            )
            BEGIN
                UPDATE Stationery
                SET stationery_price = new_price
                WHERE stationery_id = stationery_id;
            END;
        '''))

        # Stored procedure: DeleteStationeryById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteStationeryById(
                IN stationery_id INT
            )
            BEGIN
                DELETE FROM Stationery
                WHERE stationery_id = stationery_id;
            END;
        '''))

        db.session.commit()

    except Exception as e:
        print(f"Error creating stored procedure: {e}")

    


    app.run(debug=True)
    app.logger.debug(f'Current quantity of item {item_id} is {current_quantity}')
