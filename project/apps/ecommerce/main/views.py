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


@mod.route('/addto_basket/<id>')
def addto_basket(id):
    product = Product.query.filter_by(id=id).first()
    cart_id = request.cookies.get('shopping_cart')
    resp = make_response(jsonify({"status":"success",
                                  "price":str(product.price)}))
    if not cart_id:
        if current_user.is_authenticated:
            cart = Basket.query.filter_by(user_id=current_user.id).first()
            if not cart:
                cart = Basket(user_id=current_user.id)
                db.session.add(cart)
                db.session.flush()
        else:
            cart = Basket()
            db.session.add(cart)
            db.session.flush()
            resp.set_cookie('shopping_cart', value=str(cart.id), expires=cart.expires)
    else:
        cart = Basket.query.filter_by(id=cart_id).first()
    cart.add_product(id, 1)
    db.session.add(cart)
    db.session.commit()
    return resp


@mod.route('/basket')
def current_basket():
    if current_user.is_authenticated:
        basket = Basket.query.filter_by(user_id=current_user.id).first()
    else:
        basket = Basket.query.filter_by(id=request.cookies.get('shopping_cart')).first()
    return render_template('ecommerce/basket.html', basket=basket)