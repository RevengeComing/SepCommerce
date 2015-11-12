from flask import (render_template, redirect, url_for, abort, flash, request,
    current_app, make_response, Blueprint, send_from_directory, jsonify)
from flask.ext.login import login_required, current_user
from project.extensions import db
from project.apps.auth.models import Permission, Role, User
import json
import random
from .decorators import admin_required, permission_required
from  sqlalchemy.sql.expression import func, select

mod = Blueprint('main', __name__, url_prefix='/')

@mod.route('')
def index():
    return render_template('index.html')


# @mod.route('user/<username>')
# @mod2.route('user/<username>')
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     if user.role_id == 3 :
#     	return render_template('user.html', user=user)
#     if user.role_id == 4 :
#     	return render_template('grammy/producer_profile.html', user=user)
#     if user.role_id == 5 :
#     	return render_template('grammy/artist_profile.html', user=user)
#     else:
#     	return render_template("errors/404.html")


@mod.route('genre/<genreName>')
def genreIndex(genreName):
    return render_template('genreIndex.html')
