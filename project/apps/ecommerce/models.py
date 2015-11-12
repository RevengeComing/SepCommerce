from datetime import datetime
from project.extensions import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Integer)    
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    count = db.Column(db.Integer)

    category = db.relationship('ProductCategory', backref='product', lazy='dynamic')


class ProductCategory(db.Model):
	__tablename__ = 'product_categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)


class Order(db.Model):
	__tablename__ = 'orders'
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime(), default=datetime.utcnow)
	is_arrived = db.Column(db.Boolean, default=False)
	for_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	for_user = db.relationship('User', backref="orders")


class OrderedProducts(db.Model):
	__tablename__ = 'ordered_products'
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, index=True)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
