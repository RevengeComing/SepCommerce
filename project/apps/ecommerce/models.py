from datetime import datetime
from project.extensions import db
from project.apps.ecommerce.utils import set_expire_time
from flask import url_for


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Integer)    
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    count = db.Column(db.Integer)
    offer = db.Column(db.Integer, default=0)
    image = db.Column(db.String(128))

    category = db.relationship('ProductCategory', backref='products', lazy='joined')

    def get_image(self):
    	if self.image:
    		return self.image
    	else:
    		return "/statics/img/requirements.jpg"

    def self_url(self):
    	return url_for('commerce.product_page', id=self.id)

    def addto_basket_url(self):
    	return url_for('commerce.addto_basket', id=self.id)


class ProductCategory(db.Model):
	__tablename__ = 'product_categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	parent_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))

	parent = db.relationship('ProductCategory', remote_side=[id], uselist=False, backref='childs')


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


class Basket(db.Model):
	__tablename__ = "baskets"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	expires = db.Column(db.DateTime(), default=set_expire_time() )

	user = db.relationship('User', backref='basket', lazy="joined")

	def add_product(self, id, count):
		product_in_basket = ProductInBasket(basket_id=self.id,
											product_id=id,
											count=count)
		db.session.add(product_in_basket)

	def total_price(self):
		price = 0
		for product in self.products:
			price += product.count * product.price
		return price


class City(db.Model):
	__tablename__ = "cities"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)


class ProductInBasket(db.Model):
	__tablename__ = "products_in_baskets"
	id = db.Column(db.Integer, primary_key=True)
	basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
	count = db.Column(db.Integer)

	basket = db.relationship('Basket', backref='products', lazy='joined')
	product = db.relationship('Product', lazy='joined')
