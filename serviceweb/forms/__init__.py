# XXX doing too much work here, needs to simplify form gen..
from datetime import timedelta

from wtforms import Form, fields
from wtforms.csrf.session import SessionCSRF

from flask import g, session, current_app
from serviceweb.util import fullname
from serviceweb.forms.customfields import (DynamicSelectField, JsonListField,
                                           LargeTextAreaField)


_FORMS = {}


def get_form(name):
    return _FORMS[name]


class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_time_limit = timedelta(minutes=20)

        @property
        def csrf_secret(self):
            key = current_app.config['CSRF_SECRET_KEY']
            return bytes(key, 'ascii')

        @property
        def csrf_context(self):
            return session

    def label(self, entry):
        return entry['name']


def _get_users(team=None):
    if team is not None:
        filters = [{'name': 'name', 'op': 'eq', 'val': team}]
        team_id = g.db.get_entries('team', filters=filters)[0]['id']
        filter1 = {'name': 'team_id', 'op': 'eq', 'val': team_id}
        filter2 = {'name': 'secondary_team_id', 'op': 'eq', 'val': team_id}
        filters = [{"or": [filter1, filter2]}]
    else:
        filters = [{'name': 'mozqa', 'op': 'eq', 'val': True}]

    # XXX this call should be cached
    entries = g.db.get_entries('user', filters=filters, sort='firstname')
    res = [(entry.id, fullname(entry)) for entry in entries]
    res.insert(0, (-1, 'N/A'))
    return res


def get_devs():
    return _get_users('Dev')


def get_qa():
    return _get_users('QA')


def get_ops():
    return _get_users('OPS')


def get_users():
    return _get_users()


def get_teams():
    # XXX this call should be cached
    entries = g.db.get_entries('team', sort='name')
    return [(entry.id, entry.name) for entry in entries]


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
    if table == 'testrail':
        return '%(project_id)s @ %(test_rail_server)s' % entry
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
    jenkins_pipeline = fields.BooleanField()
    public = fields.BooleanField()


_FORMS['project_test'] = ProjectTestForm


class JenkinsJobForm(BaseForm):
    name = fields.StringField()
    jenkins_server = fields.StringField()
    public = fields.BooleanField()


_FORMS['jenkins_job'] = JenkinsJobForm


class TestRailForm(BaseForm):
    project_id = fields.IntegerField()
    test_rail_server = fields.StringField()
    public = fields.BooleanField()


_FORMS['testrail'] = TestRailForm


class TagForm(BaseForm):
    name = fields.StringField()


_FORMS['tag'] = TagForm
_DESC = 'To delete entries, uncheck them and submit the form.'


class ProjectForm(BaseForm):
    name = fields.StringField()
    homepage = fields.StringField()
    description = fields.TextAreaField()
    long_description = LargeTextAreaField(description='You can use Markdown.')
    public = fields.BooleanField()
    # xXXX filter by itermediate table
    #
    repositories = JsonListField('repositories',
                                 checkbox_label=display_entry,
                                 table='link',
                                 description=_DESC)
    tags = JsonListField('tags', description=_DESC)
    languages = JsonListField('languages', checkbox_label=display_entry,
                              description=_DESC)
    tests = JsonListField('tests', checkbox_label=display_entry,
                          table='project_test', relation_field='project_id',
                          description=_DESC)
    jenkins_jobs = JsonListField('jenkins_job', relation_field='project_id',
                                 description=_DESC)
    testrail = JsonListField('testrail', relation_field='project_id',
                             checkbox_label=display_entry,
                             description=_DESC)
    deployments = JsonListField('deployments', checkbox_label=display_entry,
                                relation_field='project_id',
                                description=_DESC)
    irc = fields.StringField()
    bz_product = fields.StringField()
    bz_component = fields.StringField()
    qa_group_name = DynField('qa_group', choices=get_groups, coerce=str)
    qa_primary_id = DynField('qa_primary', choices=get_qa)
    qa_secondary_id = DynField('qa_secondary', choices=get_qa)
    op_primary_id = DynField('op_primary', choices=get_ops)
    op_secondary_id = DynField('op_secondary', choices=get_ops)
    dev_primary_id = DynField('dev_primary', choices=get_devs)
    dev_secondary_id = DynField('dev_secondary', choices=get_devs)


_FORMS['project'] = ProjectForm


class LinkForm(BaseForm):
    url = fields.StringField()
    name = fields.StringField()
    public = fields.BooleanField()


_FORMS['link'] = LinkForm


class DeploymentForm(BaseForm):
    name = fields.StringField()
    endpoint = fields.StringField()
    public = fields.BooleanField()


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
    team_id = DynField('team', choices=get_teams)
    secondary_team_id = DynField('secondary_team', choices=get_teams)

    def label(self, entry):
        return fullname(entry)


_FORMS['user'] = UserForm
