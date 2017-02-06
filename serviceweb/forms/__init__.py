# XXX doing too much work here, needs to simplify form gen..
from wtforms import Form, fields
from flask import g
from serviceweb.util import fullname
from serviceweb.forms.customfields import (DynamicSelectField, JsonListField,
                                           LargeTextAreaField)


_FORMS = {}


def get_form(name):
    return _FORMS[name]


class BaseForm(Form):
    def label(self, entry):
        return entry['name']


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


def display_entry(table, entry):
    if table == 'deployment':
        return '%(name)s deployed at %(endpoint)s' % entry
    if table == 'link':
        if entry['name'] is not None:
            return '%(name)s -- %(url)s' % entry
        return entry['url']
    if table == 'language':
        name = entry['name']
        version = entry.get('version')
        if version:
            name += ' ' + version
        return name

    # trying default stuff
    if 'name' in entry:
        return entry['name']

    return entry['id']


def DynField(name, coerce=int, choices=get_users):
    return DynamicSelectField(name, coerce=coerce, choices=choices)


class LangForm(BaseForm):
    name = fields.StringField()
    version = fields.StringField()


_FORMS['language'] = LangForm


class ProjectTestForm(BaseForm):
    name = fields.StringField()
    url = fields.StringField()
    operational = fields.BooleanField()


_FORMS['project_test'] = ProjectTestForm


class TagForm(BaseForm):
    name = fields.StringField()


_FORMS['tag'] = TagForm


class ProjectForm(BaseForm):
    name = fields.StringField()
    homepage = fields.StringField()
    description = fields.TextAreaField()
    long_description = LargeTextAreaField(description='You can use Markdown.')
    # xXXX filter by itermediate table
    #
    repositories = JsonListField('repositories',
                                 checkbox_label=display_entry,
                                 table='link')
    tags = JsonListField('tags')
    languages = JsonListField('languages', checkbox_label=display_entry)
    tests = JsonListField('tests', checkbox_label=display_entry,
                          table='project_test', relation_field='project_id')
    jenkins_jobs = JsonListField('jenkins_jobs', relation_field='project_id')
    deployments = JsonListField('deployments', checkbox_label=display_entry,
                                relation_field='project_id')
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


_FORMS['project'] = ProjectForm


class LinkForm(BaseForm):
    url = fields.StringField()
    name = fields.StringField()


_FORMS['link'] = LinkForm


class DeploymentForm(BaseForm):
    name = fields.StringField()
    endpoint = fields.StringField()


_FORMS['deployment'] = DeploymentForm


class UserForm(BaseForm):
    firstname = fields.StringField()
    lastname = fields.StringField()
    mozqa = fields.BooleanField()
    github = fields.StringField()
    editor = fields.BooleanField()
    email = fields.StringField()
    irc = fields.StringField()
    mozillians_login = fields.StringField()

    def label(self, entry):
        return fullname(entry)


_FORMS['user'] = UserForm