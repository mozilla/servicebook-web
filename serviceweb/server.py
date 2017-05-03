import time
import os
import logging.config

from flask import Flask, g, render_template
from flask_bootstrap import Bootstrap
from flask_iniconfig import INIConfig
from flaskext.markdown import Markdown

from serviceweb.nav import nav
from serviceweb.search import Search
from serviceweb.views import blueprints
from serviceweb.auth import get_user, GithubAuth
from serviceweb.views.auth import unauthorized_view
from serviceweb.mozillians import Mozillians
from serviceweb.translations import APP_TRANSLATIONS
from serviceweb.util import fullname as _fullname
from serviceweb.util import testing_completion
from serviceweb.forms import display_entry as _de

from restjson.client import Client
import humanize


HERE = os.path.dirname(__file__)
DEFAULT_INI_FILE = os.path.join(HERE, '..', 'serviceweb.ini')
_DEBUG = True


class PrivacyAwareClient(Client):
    def __init__(self, app, *args, **kw):
        super(PrivacyAwareClient, self).__init__(*args, **kw)
        self.app = app

    def _post_filter(self, table, entries):
        if g.user_in_mozteam:
            return entries
        filtered = []
        for entry in entries:
            if table == 'user':
                if entry.public:
                    filtered.append(entry)
            elif table == 'project':
                for field in ('qa_primary', 'qa_secondary',
                              'op_primary', 'op_secondary',
                              'dev_primary', 'dev_secondary'):
                    if field in entry and not entry[field]['public']:
                        entry[field] = None
                filtered.append(entry)
        return filtered

    # bypass privacy
    def _get_entries(self, table, filters=None, sort=None):
        return super(PrivacyAwareClient, self).get_entries(table, filters,
                                                           sort)

    def get_entries(self, table, filters=None, sort=None):
        entries = super(PrivacyAwareClient, self).get_entries(table, filters,
                                                              sort)
        return self._post_filter(table, entries)

    def get_entry(self, table, entry_id, bust_cache=False):
        res = super(PrivacyAwareClient, self).get_entry(table, entry_id,
                                                        bust_cache)
        res = self._post_filter(table, [res])
        if len(res) == 0:
            return None
        return res[0]


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

    service_book = os.environ.get('SERVICEBOOK', None)
    if service_book is None:
        service_book = app.config['common']['service_book']

    app.db = PrivacyAwareClient(app, service_book, cache=False)
    app.search = Search(service_book)
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
        g.search = app.search
        g.user = get_user(app)
        if g.user is not None:
            team_id = g.user.get('team_id')
            secondary_team_id = g.user.get('secondary_team_id')
            # cache
            teams = [team.id for team in g.db._get_entries('team')
                     if team.name in ('OPS', 'QA', 'Dev')]

            g.user_in_mozteam = (team_id in teams or secondary_team_id in teams
                                 or g.user.get('editor'))
        else:
            g.user_in_mozteam = False

    @app.template_filter('humanize')
    def _humanize(last_modified):
        age = time.time() - (last_modified / 1000.)
        return humanize.naturaltime(age)

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

    @app.template_filter('display_entry')
    def display_entry(entry, table):
        return _de(table, entry)

    @app.errorhandler(404)
    def _404(err):
        return render_template('_404.html')

    logging.config.fileConfig(ini_file)
    return app


def main():
    app = create_app()
    app.run(debug=_DEBUG, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
