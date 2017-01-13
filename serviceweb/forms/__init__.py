from wtforms import Form, fields
from flask import g
from serviceweb.util import fullname
from serviceweb.forms.customfields import (DynamicSelectField, JsonListField,
                                           LargeTextAreaField)


def get_users():
    # only mozqa folks can be primary/secondary/group lead
    # XXX this call should be cached
    filters = [{'name': 'mozqa', 'op': 'eq', 'val': True}]
    entries = g.db.get_entries('user', filters=filters, sort='firstname')
    res = [(entry.id, fullname(entry)) for entry in entries]
    res.insert(0, (-1, 'N/A'))
    return res


def get_groups():
    # XXX this call should be cached
    entries = g.db.get_entries('group', sort='name')
    return [(entry.name, entry.name) for entry in entries]


def get_projects():
    # XXX this call should be cached
    projects = g.db.get_entries('project', sort='name')
    return [(entry.id, entry) for entry in projects]


def display_repo(entry):
    if entry['name'] is not None:
        return '%(name)s -- %(url)s' % entry
    return entry['url']


def display_lang(entry):
    data = dict(entry)
    if data['version'] is None:
        data['version'] = ''
    res = '%(name)s %(version)s' % data
    return res.strip()


def DynField(name, coerce=int, choices=get_users):
    return DynamicSelectField(name, coerce=coerce, choices=choices)


class ProjectForm(Form):
    name = fields.StringField()
    homepage = fields.StringField()
    description = LargeTextAreaField()
    repositories = JsonListField('repositories',
                                 checkbox_label=display_repo)
    tags = JsonListField('tags')
    languages = JsonListField('languages', checkbox_label=display_lang)
    tests = JsonListField('tests')
    jenkins_jobs = JsonListField('jenkins_jobs')
    irc = fields.StringField()
    bz_product = fields.StringField()
    bz_component = fields.StringField()
    qa_group_name = DynField('qa_group', choices=get_groups, coerce=str)
    qa_primary_id = DynField('qa_primary')
    qa_secondary_id = DynField('qa_secondary')
    op_primary_id = DynField('op_primary')
    op_secondary_id = DynField('op_secondary')
    dev_primary_id = DynField('dev_primary')
    dev_secondary_id = DynField('dev_secondary')


class DeploymentForm(Form):
    name = fields.StringField()
    endpoint = fields.StringField()


class UserForm(Form):
    firstname = fields.StringField()
    lastname = fields.StringField()
    mozqa = fields.BooleanField()
    github = fields.StringField()
    editor = fields.BooleanField()
    email = fields.StringField()
