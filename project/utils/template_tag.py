# -*- coding: utf-8 -*-
from project.apps.ecommerce.models import ProductCategory, Product

def index_categories():
	return ProductCategory.query.filter_by(parent_id=None)

def index_products():
	return Product.query.all()


def init_filters(app):
	app.jinja_env.globals['index_categories'] = index_categories
	app.jinja_env.globals['index_products'] = index_products