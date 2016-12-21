from flask import render_template
from flask import Blueprint
from flask import request, redirect

from serviceweb.auth import only_for_editors


users_bp = Blueprint('users', __name__)


@users_bp.route("/users/<int:user_id>")
def user_view(user_id):
    user = users_bp.app.db.get_entry('user', user_id)
    mozillians = users_bp.app.extensions['mozillians']

    if user['email']:
        mozillian = mozillians.get_info(user['email'])
    else:
        mozillian = {}

    # should be an attribute in the user table
    filters = [{'or': [{'name': 'primary_id', 'op': 'eq', 'val': user_id},
                       {'name': 'secondary_id', 'op': 'eq', 'val': user_id}]}]

    projects = users_bp.app.db.get_entries('project', filters)['objects']

    backlink = '/'
    return render_template('user.html', projects=projects, user=user,
                           backlink=backlink, mozillian=mozillian)


@users_bp.route("/users")
@only_for_editors
def users_view():
    users = users_bp.app.db.search_users()['objects']
    return render_template('users.html', users=users)


@users_bp.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
@only_for_editors
def edit_user(user_id):
    user = users_bp.app.db.get_entry('user', user_id)

    form = UserForm(request.form, user)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        Session.add(user)
        Session.commit()
        return redirect('/users')

    action = 'Edit %r' % user
    return render_template("edit.html", form=form, action=action,
                           form_action='/users/%d/edit' % user.id,
                           backlink='/users/%d' % user.id)
