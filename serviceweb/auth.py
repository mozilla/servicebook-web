from functools import wraps

from rauth.service import OAuth2Service
from flask import session, abort, g


def GithubAuth(app):
    github = OAuth2Service(**app.config['oauth'])
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    app.extensions['github'] = github


def github2dbuser(github_user):
    filters = [{'name': 'github',
                'op': 'eq',
                'val': github_user['login']}]
    res = g.db.get_entries('user', filters=filters)

    if res['num_results'] > 0:
        db_user = res['objects'][0]
    else:
        # creating an entry
        name = github_user['name'].split(' ', 1)
        if len(name) == 2:
            firstname, lastname = name
        else:
            firstname = lastname = name

        login = github_user['login']
        user = {'github': login, 'firstname': firstname,
                'lastname': lastname,
                'mozqa': False, 'editor': False}
        db_user = g.db.create_entry('user', user)

    return db_user


def get_user(app):
    if 'token' not in session:
        return None

    github = app.extensions['github']
    auth = github.get_session(token=session['token'])
    resp = auth.get('/user')
    if resp.status_code == 200:
        user = resp.json()
        return github2dbuser(user)
    else:
        return None


def only_for_editors(func):
    @wraps(func)
    def _only_for_editors(*args, **kw):
        user = g.user

        if user is None:
            if g.debug:
                print('Anonymous rejected')
            abort(401)
            return

        if not user['editor']:
            if g.debug:
                print('%r rejected' % user)
            abort(401)
            return

        return func(*args, **kw)
    return _only_for_editors
