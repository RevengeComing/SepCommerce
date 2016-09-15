from flask import (render_template, make_response, request, redirect,
    jsonify, url_for)
from flask.ext.login import current_user

from project.extensions import db
from project.apps.ecommerce import mod
from project.apps.ecommerce.models import Product, Basket

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
        basket = current_user.basket[0]
    else:
        basket = Basket.query.filter_by(id=request.cookies.get('shopping_cart')).first()
    return render_template('ecommerce/basket.html', basket=basket)


@mod.route('/update_basket', methods=["POST"])
def update_basket():
    if current_user.is_authenticated:
        basket = current_user.basket[0]
    else:
        basket = Basket.query.filter_by(id=request.cookies.get('shopping_cart')).first()

    basket.update_product(int(request.form.get('product_id')),
    					  int(request.form.get('product_count')))
    return "success"


@mod.route('/remove_from_basket/<product_id>')
def remove_from_basket(product_id):
	if current_user.is_authenticated:
		basket = current_user.basket[0]
	else:
		basket = Basket.query.filter_by(id=request.cookies.get('shopping_cart')).first()
		if basket == None :
			return 'None'
	basket.remove_from_basket(product_id)
	return redirect(url_for('commerce.current_basket'))
