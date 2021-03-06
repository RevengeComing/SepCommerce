from flask import render_template, redirect, request, url_for, flash, current_app, make_response
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import mod
from project.extensions import db
from .models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
 PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from project.apps.ecommerce.models import remove_cart, Basket


@mod.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@mod.route('/unconfirmed')
def unconfirmed():
    return render_template('auth/unconfirmed.html')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if current_user.role.name == 'Administrator':
                resp = make_response(redirect(url_for('admin.index')))
                remove_cart(resp)
                return resp
            resp = make_response(redirect(request.args.get('next') or url_for('main.index', username=current_user.username)))
            id = request.cookies.get('shopping_cart')
            if id:
                user_cart = Basket.query.filter_by(user_id=user.id).first()
                if user_cart:
                    resp.set_cookie('shopping_cart', '', expires=0)
                    cart = Basket.query.filter_by(id=id).first()
                    for product in cart.products:
                        product.basket_id = user_cart.id
                    db.session.commit()
                    db.session.delete(cart)
                else:
                    resp.set_cookie('shopping_cart', '', expires=0)
                    cart = Basket.query.filter_by(id=id).first()
                    cart.user_id = user.id
                    user.basket_id = id
                    db.session.commit()
            return resp
        else:
            return render_template('auth/login.html',
                                   form=form,
                                   error_message='Username or password is wrong.')
    return render_template('auth/login.html', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    resp = make_response(redirect(request.referrer or url_for('main.index')))
    # resp.set_cookie('shopping_cart', '', expires=0)
    return resp


@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        print "asghar"
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        if not form.email.data == current_app.config['ADMIN']:
            send_email(user.email, 'Confirm Your Account',
                       'auth/email/confirm', user=user, token=token)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@mod.route('/confirm/<token>')
# @login_required
def confirm(token):
    print "asghar"
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        print "asghar"
    else:
        pass
    return redirect(url_for('main.index'))


@mod.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@mod.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@mod.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@mod.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@mod.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@mod.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))