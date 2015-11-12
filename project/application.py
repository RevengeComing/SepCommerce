import logging
import logging.handlers

from flask import Flask
from flask import g
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import render_template

from project.config import DefaultConfig as base_config
from gettext import gettext as _

# from project.apps.models import User

from project.extensions import  db, mail, login_manager
# from flask.ext import breadcrumbs

#from project.utils.issue import import_cart_to_list
__all__ = ['create_app', 'create_simple_app']

DEFAULT_APP_NAME = 'project'


def create_app(config=None, app_name=DEFAULT_APP_NAME):
    """
    Tabe asli hast ke app ro misaze va configesh mikone.
    be in tabe tanzimate barname tahte name config ersal mishe va on tabzimat dar dakhele object
    app zakhire va negahdari mishe

    @param config: class ya objecte haviye tanzimate kolliye app mibashad.
    @param app_name: name asliye narm afzar
    """

    #TODO: static_folder va template_folder bayad dar method joda set beshe
    app = Flask(app_name, static_folder='media/statics', template_folder='media/templates')
    # breadcrumbs.Breadcrumbs(app=app)

    configure_app(app, config)
    configure_blueprints(app)
    configure_template_tag(app)
    # configure_logger(app)
    # configure_user(app)
    configure_extentions(app)
    # configure_site(app)
    # configure_request(app)
    return app


def configure_app(app, config):
    """
    tanzimate kolli app ke mamolan dar yek file zakhore mishavat tavasote in tabe
    megdar dehi va load mishavad
    """

    # config default ro dakhele app load mikone
    app.config.from_object(base_config())
    #sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    if config is not None:
        # agar config degari be create_app ersal shode bashe dar in bakhsh load mishe
        # agar tanzimate in bakhsh gablan va dakhele defalt config tanzim shode bashe dobare nevisi mishe
        app.config.from_object(config)
    # dar sorati ke environment variable baraye tanzimat set shode bashe ham load mishe
    app.config.from_envvar('project_CONFIG', silent=True)


def configure_blueprints(app):
    """
    Tanzimate marbot be blueprint ha va load kardan ya nasbe onha ro inja anjam midim
    """

    app.config.setdefault('INSTALLED_BLUEPRINTS', [])
    blueprints = app.config['INSTALLED_BLUEPRINTS']
    for blueprint_name in blueprints:

        bp = __import__('project.apps.%s' % blueprint_name, fromlist=['views'])

        try:
            app.register_blueprint(bp.views.mod)
        except:
            # report has no views
            pass

def configure_errorhandlers(app):
    """
    tavasote in method baraye error haye asli va mamol khatahaye monaseb bargasht dade mishavad
    """

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        #import_cart_to_list(error)
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found')), 404

        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(402)
    def payment_required(error):
        #import_cart_to_list(error)
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed')), 402
        return render_template("errors/402.html", error=error), 402

    @app.errorhandler(403)
    def forbidden(error):
        #import_cart_to_list(error)
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed')), 403
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(500)
    def server_error(error):
        #import_cart_to_list(error)
        if request.is_xhr:
            #import_cart_to_list(error)
            return jsonify(error=_('Sorry, an error has occurred')), 500
        return render_template("errors/500.html", error=error), 500

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error=_("Login required"))
        return redirect(url_for("profile.login", next=request.path))



def configure_template_tag(app):
    from project.utils.template_tag import init_filters
    init_filters(app)

def configure_extentions(app):
    db.init_app(app)
    # auth.init_app(app,user_model=User)
    mail.init_app(app)
    login_manager.init_app(app)
    # cache.init_app(app)

# def configure_site(app):
#     """
#     """
#     @app.context_processor
#     def site_default():
#         """
#         """
#         return {
#             'site_name': current_site()['title'],
#             'debug': app.config['DEBUG']
#             }

    # @app.context_processor
    # def login_form():
    #     """
    #     """
    #     if not g.user.has_group('guest'):
    #         return {}
    #     return {'login_form': Auth.login()}


# def configure_logger(app):
#     """
#     This function Configure Logger for given Application.

#     :param app: Application Object
#     :type app: Object
#     """

#     # from project.utils.extended_logging import wrap_app_logger
#     # wrap_app_logger(app)
#     if app.debug or app.testing:
#         from project.utils.extended_logging import wrap_app_logger
#         wrap_app_logger(app)
#         app.logger.create_logger('debuging')
#         return

#     formatter = logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s '
#         '[in %(pathname)s:%(lineno)d]')

#     debug_file_handler = logging.handlers.RotatingFileHandler(
#         app.config['DEBUG_LOG'],
#         maxBytes=100000,
#         backupCount=10)

#     debug_file_handler.setLevel(logging.DEBUG)
#     debug_file_handler.setFormatter(formatter)
#     app.logger.addHandler(debug_file_handler)

#     error_file_handler = logging.handlers.RotatingFileHandler(
#         app.config['ERROR_LOG'],
#         maxBytes=100000,
#         backupCount=10)

#     error_file_handler.setLevel(logging.ERROR)
#     error_file_handler.setFormatter(formatter)
#     app.logger.addHandler(error_file_handler)


# def configure_user(app):

#     @app.before_request
#     def before_request():
#         """
#         """
#         if 'username' in session:
#             try:
#                 g.user = User.select(User.username==session.get('username')).get()
#             except:
#                 g.user = GuestUser()
#         else:
#             g.user = GuestUser()

# def configure_request(app):

#     @app.before_request
#     def breadcrumbs_config():
#         g.breadcrumbs = [{'url': '/', 'title': 'Node List'}]