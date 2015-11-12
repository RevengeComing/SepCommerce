from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()