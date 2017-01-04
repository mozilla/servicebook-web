from wtforms import (Form, BooleanField, StringField, TextField,
                     SelectField)
from flask import g
from serviceweb.util import fullname


def get_users():
    # only mozqa folks can be primary/secondary/group lead
    # XXX this call should be cached
    filters = [{'name': 'mozqa', 'op': 'eq', 'val': True}]
    entries = g.db.get_entries('user', filters=filters, order_by='firstname')
    res = [(entry.id, fullname(entry)) for entry in entries['objects']]
    res.insert(0, (-1, 'N/A'))
    return res


def get_groups():
    # XXX this call should be cached
    entries = g.db.get_entries('group', order_by='name')['objects']
    return [(entry.name, entry.name) for entry in entries]


def get_projects():
    # XXX this call should be cached
    projects = g.db.get_entries('project', order_by='name')['objects']
    return [(entry.id, entry) for entry in projects]


class DynamicSelectField(SelectField):
    def iter_choices(self):
        choices = callable(self.choices) and self.choices() or self.choice
        for value, label in choices:
            yield (value, label, self.coerce(value) == self.data)

    def pre_validate(self, form):
        choices = callable(self.choices) and self.choices() or self.choice
        for v, _ in choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class ProjectForm(Form):
    name = StringField()
    description = TextField()
    irc = StringField()
    homepage = StringField()
    repository = StringField()
    bz_product = StringField()
    bz_component = StringField()
    qa_primary_id = DynamicSelectField('qa_primary', coerce=int,
                                       choices=get_users)
    qa_secondary_id = DynamicSelectField('qa_secondary', coerce=int,
                                         choices=get_users)
    qa_group_name = DynamicSelectField('qa_group', choices=get_groups)
    op_primary_id = DynamicSelectField('op_primary', coerce=int,
                                       choices=get_users)
    op_secondary_id = DynamicSelectField('op_secondary', coerce=int,
                                         choices=get_users)
    dev_primary_id = DynamicSelectField('dev_primary', coerce=int,
                                        choices=get_users)
    dev_secondary_id = DynamicSelectField('dev_secondary', coerce=int,
                                          choices=get_users)


class DeploymentForm(Form):
    name = StringField()
    endpoint = StringField()


class UserForm(Form):
    firstname = StringField()
    lastname = StringField()
    mozqa = BooleanField()
    github = StringField()
    editor = BooleanField()
    email = StringField()
