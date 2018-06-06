import os

from flask.helpers import get_debug_flag

"""The app module, containing the app factory function."""
from flask import Flask, render_template
from settings import DevConfig

def create_app(config_object):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    #register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    #register_commands(app)
    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    #app.register_blueprint(public.views.blueprint)
    #app.register_blueprint(quiz.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db
            }

    app.shell_context_processor(shell_context)

CONFIG = DevConfig #if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

