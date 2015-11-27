# -*- coding: utf-8 -*-
from flask import request

from project.apps.ecommerce.models import ProductCategory, Product, Basket

def index_categories():
	return ProductCategory.query.filter_by(parent_id=None)

def index_products():
	return Product.query.all()

def get_cart():
	id = request.cookies.get('shopping_cart')
	cart = Basket.query.filter_by(id=id).first()
	return cart

def init_filters(app):
	app.jinja_env.globals['index_categories'] = index_categories
	app.jinja_env.globals['index_products'] = index_products