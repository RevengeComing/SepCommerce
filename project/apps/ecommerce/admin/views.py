from flask import render_template, request, redirect, url_for, current_app
import os

from project.apps.admin import mod as adminPanel
from project.apps.ecommerce import mod

from project.apps.main.decorators import admin_required
from project.apps.ecommerce.models import ProductCategory, Product
from project.apps.ecommerce.utils import allowed_file
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

@adminPanel.route('/products/add', methods=["POST", "GET"])
@admin_required
def add_product():
	categories = ProductCategory.query.filter_by(childs=None)
	if request.method == "POST":
		name = request.form["name"]
		price = int(request.form["price"])
		count = int(request.form["count"])
		try:
			offer = int(request.form.get("offer"))
		except:
			offer = 0
		category = request.form["parent"]
		
		product = Product(name=name,
						  price=price,
						  count=count,
						  offer=offer,
						  category_id=category)

		db.session.add(product)
		db.session.flush()
		image = request.files.get('image')
		if image and allowed_file(image.filename):
			filename = str(product.id)
			image.save(os.path.realpath("project/media/statics/img/products/") +"/"+ filename)
			product.image = "/statics/img/products/" + filename
			db.session.commit()

		return redirect(url_for('admin.products'))
	return render_template('admin/add_product.html', categories=categories)