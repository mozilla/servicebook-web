from flask import Blueprint, session, flash, render_template
from serviceweb.auth import oidc2dbuser, NotRegisteredError
from serviceweb.util import safe_redirect


auth = Blueprint('auth', __name__)


@auth.route('/registration')
def registration():
    return render_template('registration.html'), 401


@auth.route('/login')
def login():
    if session.get('access_token') is None:
        session['destination'] = '/login'
        return auth.app.oidc._authenticate()

    oidc_user = session['userinfo']
    try:
        db_user = oidc2dbuser(oidc_user)
    except NotRegisteredError:
        return safe_redirect('/registration')

    session['user_id'] = db_user['id']
    # cache busting when user data changes?
    session['user'] = db_user
    flash('Logged in as ' + str(db_user))
    return safe_redirect('/')


@auth.route('/logout')
def logout():
    for field in ('access_token', 'token', 'user_id', 'user', 'userinfo'):
        if field in session:
            del session[field]
    flash('Logged out')
    return safe_redirect('/oidc/logout')


def unauthorized_view(error):
    return render_template('unauthorized.html', backlink='/'), 401
