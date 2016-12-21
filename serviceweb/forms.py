from collections import OrderedDict
from wtforms import Form, BooleanField, StringField, IntegerField


def get_users():
    # only mozqa folks can be primary/secondary/group lead
    from servicebook.db import Session
    return Session().query(User).filter(User.mozqa == True)   # noqa


def get_groups():
    from servicebook.db import Session
    return Session().query(Group).order_by(Group.name)


def get_projects():
    from servicebook.db import Session
    return Session().query(Project).order_by(Project.name)


class ProjectForm(Form):

    field_order = ('name', 'description', 'primary', 'secondary', 'group',
                   'bz_product', 'bz_component', 'irc')
    #primary = QuerySelectField('primary', query_factory=get_users)
    #secondary = QuerySelectField('secondary', query_factory=get_users)
    #group = QuerySelectField('group', query_factory=get_groups,
    #                         get_label='name')


class DeploymentForm(Form):
    name = StringField()
    endpoint = StringField()
    project_id = IntegerField()


class UserForm(Form):
    firstname = StringField()
    lastname = StringField()
    mozqa = BooleanField()
    github = StringField()
    editor = BooleanField()
    email = StringField()


