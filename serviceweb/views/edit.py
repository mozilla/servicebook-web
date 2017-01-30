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


@edit.route("/<table_name>/<int:entry_id>/add_relation/<relname>/<target>",
            methods=['GET', 'POST'])
@only_for_editors
def add_relation(table_name, entry_id, relname, target):
    tmpl = "add_relation.html"
    existing = g.db.get_entries(target)
    form = get_form(target)(request.form)
    action = '/%s/%d/add_relation/%s/%s' % (table_name, entry_id, relname,
                                            target)

    if request.method == 'POST':
        picked_entries = request.form.getlist('picked_entry')
        if picked_entries is not None:
            entry = g.db.get_entry(table_name, entry_id)
            existing_ids = [rel['id'] for rel in entry[relname]]
            changed = False
            for picked in picked_entries:
                if picked not in existing_ids:
                    entry[relname].append({'id': picked})
                    changed = True
            if changed:
                g.db.update_entry(table_name, entry)
        else:
            # creation
            raise NotImplementedError()

        return redirect('/%s/%d/edit' % (table_name, entry_id))

    return render_template(tmpl, form=form, form_action=action,
                           existing=existing, target=target)
