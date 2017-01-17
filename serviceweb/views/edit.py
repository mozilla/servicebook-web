from flask import Blueprint
from serviceweb.auth import only_for_editors
from serviceweb.forms import get_form
from flask import request, redirect, g
from flask import render_template


edit = Blueprint('edit', __name__)


@edit.route("/<table_name>/<int:entry_id>/edit", methods=['GET', 'POST'])
@only_for_editors
def edit_table(table_name, entry_id):
    inline = request.args.get('inline')
    entry = g.db.get_entry(table_name, entry_id)
    form = get_form(table_name)(request.form, entry)

    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)

        # not updating relations for now
        for field in list(entry.keys()):
            if isinstance(entry[field], (dict, list)):
                del entry[field]

        g.db.update_entry(table_name, entry)
        return redirect('/%s/%d' % (table_name, entry_id))

    action = 'Edit %r' % form.label(entry)
    backlink = '/%s/%d' % (table_name, entry_id)
    if inline is not None:
        tmpl = "inline_edit.html"
    else:
        tmpl = "edit.html"

    return render_template(tmpl, form=form, action=action, backlink=backlink,
                           form_action='/%s/%d/edit' % (table_name, entry_id))
