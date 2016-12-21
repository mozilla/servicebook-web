from flask import render_template
from flask import Blueprint


groups = Blueprint('groups', __name__)


@groups.route("/groups/<name>")
def group_view(name):
    group = groups.app.db.get_entry('group', name, 'name')

    # should be an attribute in the group table
    filters = [{'name': 'group_name', 'op': 'eq', 'val': name}]
    projects = groups.app.db.get_entries('project', filters)['objects']
    backlink = '/'
    return render_template('group.html', projects=projects, group=group,
                           backlink=backlink)
