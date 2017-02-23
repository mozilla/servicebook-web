from flask import request, render_template, g, redirect
from restjson.client import objdict


def fullname(user):
    """ Returns the full name of a user.
    """
    if not user:
        return ''
    firstname = user['firstname'].capitalize()
    lastname = user['lastname'].capitalize()
    return '%s %s' % (firstname, lastname)


def testing_completion(project):
    """Returns a completion percentage for a project.

    e.g. the percentage of tests that are marked operational
    """
    num = len(project.tests)
    if num == 0:
        return 0
    done = len([test for test in project.tests if test['operational']])
    if done == 0:
        return 0
    return int(float(done) / float(num) * 100)


def add_view(form, table, action, form_url, redirect_url, id_field='id'):
    """ Generic add form.
    """
    form = form(request.form)
    if request.method == 'POST' and form.validate():
        entry = objdict()
        form.populate_obj(entry)
        entry_id = g.db.create_entry(table, entry)[id_field]
        return redirect(redirect_url + '/%d' % entry_id)

    return render_template("edit.html", form=form, action=action,
                           form_action=form_url)
