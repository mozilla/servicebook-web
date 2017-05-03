from restjson.client import ResourceError
from flask import render_template, Blueprint, g, abort

from serviceweb.auth import only_for_editors
from serviceweb.forms import UserForm
from serviceweb.util import add_view, safe_redirect


users_bp = Blueprint('users', __name__)


@users_bp.route("/user/<int:user_id>")
def user_view(user_id):
    try:
        user = g.db.get_entry('user', user_id)
    except ResourceError:
        return abort(404)

    if user is None:
        return abort(404)

    mozillians = users_bp.app.extensions['mozillians']

    if user['mozillians_login']:
        mozillian = mozillians.get_info(user['mozillians_login'])
    else:
        mozillian = {}

    # should be an attribute in the user table
    filters = []
    for role in ('qa_primary_id', 'qa_secondary_id', 'op_primary_id',
                 'op_secondary_id', 'dev_primary_id', 'dev_secondary_id'):
        filters.append({'name': role, 'op': 'eq', 'val': user_id})

    filters = [{'or': filters}]
    projects = g.db.get_entries('project', filters)
    backlink = '/'
    return render_template('user.html', projects=projects, user=user,
                           backlink=backlink, mozillian=mozillian)


@users_bp.route("/user/<int:user_id>/delete")
@only_for_editors
def users_delete(user_id):
    try:
        g.db.get_entry('user', user_id)
    except ResourceError:
        return abort(404)
    g.db.delete_entry('user', user_id)
    return safe_redirect('/user')


@users_bp.route("/user")
@only_for_editors
def users_view():
    users = g.db.get_entries('user')

    # XXX should be pulled with a single call
    def get_teams(user):
        if user.team_id:
            filters = [{'name': 'id', 'op': 'eq',
                        'val': user.team_id}]
            filters = [{'or': filters}]
            teams = g.db.get_entries('team', filters)
            user.team = teams[0]

        if user.secondary_team_id:
            filters = [{'name': 'id', 'op': 'eq',
                        'val': user.secondary_team_id}]
            filters = [{'or': filters}]
            teams = g.db.get_entries('team', filters)
            user.secondary_team = teams[0]

        return user

    users = [get_teams(user) for user in users]

    return render_template('users.html', users=users)


@users_bp.route("/adduser", methods=["GET", "POST"])
@only_for_editors
def add_user():
    return add_view(UserForm, 'user', 'Add a new user', '/adduser',  '/user')
