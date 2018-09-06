import os
from urllib.parse import urlparse
from functools import wraps
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask import session, abort, g, jsonify, request, flash


class ScopedAuth(OIDCAuthentication):
    def _do_userinfo_request(self, state, userinfo_endpoint_method):
        if userinfo_endpoint_method is None:
            return None
        func = self.client.do_user_info_request
        return func(method=userinfo_endpoint_method, state=state,
                    scope='openid profile')


class NotRegisteredError(Exception):
    pass


def oidc2dbuser(oidc_user):
    # got an email, looking in the DB
    if 'email' in oidc_user:
        email = oidc_user['email']
        filters = [{'name': 'email', 'op': 'eq', 'val': email}]
        res = g.db.get_entries('user', filters=filters)
        if len(res) == 1:
            return res[0]
    else:
        email = ''
    # not creating entries automatically for now
    raise NotRegisteredError(email)


def get_user(app):
    is_dev = os.environ.get('FLASK_ENV') == 'development'

    def print_dev(msg):
        if not is_dev:
            return
        print('[auth debug] ' + msg)

    if 'user' in session:
        print_dev('user already in session')
        return session['user']

    remote = request.remote_user or os.environ.get('REMOTE_USER')
    if not remote:
        remote = request.headers.get('OIDC_CLAIM_ID_TOKEN_EMAIL')

    if remote:
        print_dev('got a remote user %s' % remote)
        filters = [{'name': 'email', 'op': 'eq', 'val': remote}]
        res = g.db.get_entries('user', filters=filters)
        if len(res) == 1:
            print_dev('got one match in the db')
            db_user = res[0]
            session['user_id'] = db_user['id']
            session['user'] = db_user
            flash('Logged in as ' + str(db_user))
            return db_user
        else:
            print_dev('no match')

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


class OIDConnect(object):
    def __init__(self, app, **config):
        self.domain = config['domain']
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.redirect_uri = config.get('redirect_uri', '/auth0')
        self.login_url = "https://%s/login?client=%s" % (
            self.domain, self.client_id

        )
        self.auth_endpoint = "https://%s/authorize" % self.domain
        self.token_endpoint = "https://%s/oauth/token" % self.domain
        self.userinfo_endpoint = "https://%s/userinfo" % self.domain
        self.app = app
        self.ready = False

    def set_auth(self):
        if self.ready:
            return
        provider = self.provider_info()
        client = self.client_info()
        parse_url = urlparse(self.redirect_uri)

        xtra = {"scope": ["openid", "profile", "email"]}
        self.oidc = ScopedAuth(self.app,
                               provider_configuration_info=provider,
                               client_registration_info=client,
                               extra_request_args=xtra)

        self.app.add_url_rule(parse_url.path, 'redirect_oidc',
                              self.oidc._handle_authentication_response)

        with self.app.app_context():
            url = self.redirect_uri
            self.oidc.client_registration_info['redirect_uris'] = url
            self.oidc.client.registration_response['redirect_uris'] = url

            @self.oidc.error_view
            def error(error=None, error_description=None):
                return jsonify({'error': error, 'message': error_description})

        self.app.oidc = self.oidc
        self.ready = True

    def client_info(self):
        return {'client_id': self.client_id,
                'client_secret': self.client_secret}

    def provider_info(self):
        return {'issuer': self.domain,
                'authorization_endpoint': self.auth_endpoint,
                'token_endpoint': self.token_endpoint,
                'userinfo_endpoint': self.userinfo_endpoint}
