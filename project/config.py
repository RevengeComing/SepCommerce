# coding: utf-8


class DefaultConfig(object):
    MINIFY = False

    SECRET_KEY = 'sepCommerce'

    # Blueprint haye nasb shode dar app bayad be in list ezafe beshan
    INSTALLED_BLUEPRINTS = (
        'auth',
        'admin',
        'main'
    )

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "gramatune@gmail.com"
    MAIL_PASSWORD = "nimasepehr123"
    MAIL_SUBJECT_PREFIX = "[SepCommerce]"
    MAIL_SENDER = "SepCommerce Admin <gramatune@gmail.com>"

    ADMIN = "s.hamzelooy@gmail.com"

    CACHE_TYPE = 'filesystem'
    CACHE_DIR = "/tmp/cache"



class DeploymentConfig(DefaultConfig):
    POSTGRES_HOST =  '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'postgres://sepehr:1234@%s/sepCommerce' % POSTGRES_HOST
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    POSTGRES_HOST =  '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'postgres://sepehr:1234@%s/sepCommerce' % POSTGRES_HOST
    DEBUG = True
