# coding: utf-8


class DefaultConfig(object):
    MINIFY = False

    SECRET_KEY = 'sepCommerce'

    # Blueprint haye nasb shode dar app bayad be in list ezafe beshan
    INSTALLED_BLUEPRINTS = (
        'auth',
        'ecommerce',
        'admin',
        'main',
    )

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # this email is only for testing this software.
    MAIL_USERNAME = "gramatune@gmail.com"
    MAIL_PASSWORD = "nimasepehr123"

    MAIL_SUBJECT_PREFIX = "[SepCommerce]"
    MAIL_SENDER = "SepCommerce Admin <gramatune@gmail.com>"

    ADMIN = "s.hamzelooy@gmail.com"

    CACHE_TYPE = 'filesystem'
    CACHE_DIR = "/tmp/cache"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = 'media/statics/uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


class DeploymentConfig(DefaultConfig):
    POSTGRES_HOST =  '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'postgres://sepehr:1234@%s/sepCommerce' % POSTGRES_HOST
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    POSTGRES_HOST =  '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/sepehr/Documents/Work/flask/SepCommerce/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'postgres://sepehr:1234@%s/sepCommerce' % POSTGRES_HOST
    DEBUG = True
