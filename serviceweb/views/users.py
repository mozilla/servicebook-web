from flask import render_template
from flask import Blueprint
from flask import g

from serviceweb.auth import only_for_editors


users_bp = Blueprint('users', __name__)


@users_bp.route("/user/<int:user_id>")
def user_view(user_id):
    user = g.db.get_entry('user', user_id)
    mozillians = users_bp.app.extensions['mozillians']

    if user['email']:
        mozillian = mozillians.get_info(user['email'])
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


@users_bp.route("/user")
@only_for_editors
def users_view():
    users = g.db.get_entries('user')
    return render_template('users.html', users=users)
