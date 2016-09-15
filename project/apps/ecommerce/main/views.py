from flask import (render_template, make_response, request, redirect,
    jsonify)
from flask.ext.login import current_user

from project.extensions import db
from project.apps.ecommerce import mod
from project.apps.ecommerce.models import Product, Basket


@mod.route("/product/<id>")
def product_page(id):
    product = Product.query.filter_by(id=id).first()
    return render_template('ecommerce/product.html', product=product)








