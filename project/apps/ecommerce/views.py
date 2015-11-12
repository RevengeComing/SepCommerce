from ..admin import mod as adminPanel
from project.apps.main.decorators import admin_required
from .models import ProductCategory, Product
from . import mod
from flask import render_template, request, redirect, url_for
from project.extensions import db

@adminPanel.route('/categories')
@admin_required
def categories():
	categories = ProductCategory.query.order_by(ProductCategory.id)
	return render_template('admin/categories.html', categories=categories)

@adminPanel.route('/categories/add', methods=["POST", "GET"])
@admin_required
def add_category():
	categories = ProductCategory.query.all()
	if request.method == "POST":
		name = request.form["name"]
		parent_id = request.form.get('parent')
		category = ProductCategory(name=name, parent_id=parent_id)
		db.session.add(category)
		db.session.commit()
		return redirect(url_for('admin.categories'))
	return render_template('admin/add_category.html', categories=categories)

@adminPanel.route('/products')
@admin_required
def products():
	products = Product.query.order_by(Product.id)
	return render_template('admin/products.html', products=products)