import os
import logging.config

from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_iniconfig import INIConfig
from flaskext.markdown import Markdown

from serviceweb.nav import nav
from serviceweb.views import blueprints
from serviceweb.auth import get_user, GithubAuth
from serviceweb.views.auth import unauthorized_view
from serviceweb.mozillians import Mozillians
from serviceweb.translations import APP_TRANSLATIONS

from serviceweb.util import fullname as _fullname
from serviceweb.util import testing_completion
from restjson.client import Client


HERE = os.path.dirname(__file__)
DEFAULT_INI_FILE = os.path.join(HERE, '..', 'serviceweb.ini')
_DEBUG = True


def create_app(ini_file=DEFAULT_INI_FILE):
    app = Flask(__name__, static_url_path='/static')
    INIConfig(app)
    app.config.from_inifile(ini_file)
    app.secret_key = app.config['common']['secret_key']

    Bootstrap(app)
    GithubAuth(app)
    Mozillians(app)
    Markdown(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    app.db = Client(app.config['common']['service_book'])
    app.register_error_handler(401, unauthorized_view)
    nav.init_app(app)

    app.add_url_rule(
           app.static_url_path + '/<path:filename>',
           endpoint='static',
           view_func=app.send_static_file)

    @app.before_request
    def before_req():
        g.debug = _DEBUG
        g.db = app.db
        g.user = get_user(app)

    @app.template_filter('translate')
    def translate_string(s):
        return APP_TRANSLATIONS.get(s, s)

    @app.template_filter('capitalize')
    def capitalize_string(s):
        return s[0].capitalize() + s[1:]

    @app.template_filter('completion')
    def completion(s):
        return testing_completion(s)

    @app.template_filter('fullname')
    def fullname(s):
        return _fullname(s)

    logging.config.fileConfig(ini_file)
    return app


def main():
    app = create_app()
    app.run(debug=_DEBUG, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
