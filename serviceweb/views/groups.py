from flask import render_template
from flask import Blueprint, g


groups = Blueprint('groups', __name__)


@groups.route("/groups/<name>")
def group_view(name):
    group = g.db.get_entry('group', name)

    # should be an attribute in the group table
    filters = [{'name': 'qa_group_name', 'op': 'eq', 'val': name}]
    projects = g.db.get_entries('project', filters)
    backlink = '/'
    return render_template('group.html', projects=projects, group=group,
                           backlink=backlink)
