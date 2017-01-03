import yaml
import requests

from flask import render_template
from flask import Blueprint
from flask import request, redirect, g

from serviceweb.auth import only_for_editors
from serviceweb.forms import ProjectForm, DeploymentForm
from restjson.client import objdict


projects = Blueprint('projects', __name__)


_STATUSES = 'status=NEW&status=REOPENED&status=UNCONFIRMED&status=ASSIGNED'
_BUGZILLA = ('https://bugzilla.mozilla.org/rest/bug?' + _STATUSES +
             '&product=%s&component=%s&limit=10')


@projects.route("/projects/<int:project_id>/edit", methods=['GET', 'POST'])
@only_for_editors
def edit_project(project_id):
    project = g.db.get_entry('project', project_id)
    form = ProjectForm(request.form, project)

    if request.method == 'POST' and form.validate():
        form.populate_obj(project)
        g.db.update_entry('project', project)
        return redirect('/projects/%d' % project_id)

    action = 'Edit %r' % project.name
    backlink = '/projects/%d' % project_id
    return render_template("edit.html", form=form, action=action,
                           backlink=backlink,
                           form_action='/projects/%d/edit' % project_id)


@projects.route("/projects/", methods=['GET', 'POST'])
@only_for_editors
def add_project():
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project = objdict()
        form.populate_obj(project)
        project_id = g.db.create_entry('project', project)['id']
        return redirect('/projects/%d' % project_id)

    action = 'Add a new project'
    return render_template("edit.html", form=form, action=action,
                           form_action="/projects/")


@projects.route("/projects/<int:project_id>")
def project(project_id):
    project = g.db.get_entry('project', project_id)

    # scraping bugzilla info
    if project['bz_product']:
        bugzilla = _BUGZILLA % (project['bz_product'],
                                project['bz_component'])
        try:
            res = requests.get(bugzilla)
            bugs = res.json()['bugs']
        except requests.exceptions.SSLError:
            bugs = []
    else:
        bugs = []

    # if we have some deployments, scraping project info out of the
    # stage one (fallback to the first one)
    swagger = None

    def _api(depl):
        return depl['endpoint'].lstrip('/') + '/__api__'

    if len(project['deployments']) > 0:
        for depl in project['deployments']:
            if depl['name'] == 'stage':
                swagger = _api(depl)
                break

        if swagger is None:
            swagger = _api(project['deployments'][0])

    project_info = None

    if swagger is not None:
        res = requests.get(swagger)
        if res.status_code == 200:
            project_info = yaml.load(res.content)['info']

    backlink = '/'
    edit = '/projects/%d/edit' % project['id']
    return render_template('project.html', project=project, bugs=bugs,
                           edit=edit,
                           project_info=project_info, backlink=backlink)


@projects.route("/projects/<int:project_id>/deployments",
                methods=['GET', 'POST'])
@only_for_editors
def add_deployment(project_id):
    form = DeploymentForm(request.form)
    project = g.db.get_entry('project', project_id)

    if request.method == 'POST' and form.validate():
        deployment = objdict({'project_id': project_id})
        form.populate_obj(deployment)
        g.db.create_entry('deployment', deployment)
        return redirect('/projects/%d' % project_id)

    action = 'Add a new deployment for %s' % project.name
    return render_template("edit.html", form=form, action=action,
                           form_action="/projects/%s/deployments" % project_id)


@projects.route("/projects/<int:project_id>/deployments/<int:depl_id>/delete",
                methods=['GET'])
@only_for_editors
def remove_deployment(project_id, depl_id):
    g.db.delete_entry('deployment', depl_id)
    return redirect('/projects/%d' % (project_id))


@projects.route("/projects/<int:project_id>/deployments/<int:depl_id>/edit",
                methods=['GET', 'POST'])
@only_for_editors
def edit_deployment(project_id, depl_id):
    depl = g.db.get_entry('deployment', depl_id)
    project = depl.project
    form = DeploymentForm(request.form, depl)

    if request.method == 'POST' and form.validate():
        form.populate_obj(depl)
        g.db.update_entry('deployment', depl)
        return redirect('/projects/%d' % (project_id))

    form_action = '/projects/%d/deployments/%d/edit'
    backlink = '/projects/%d' % project_id
    action = 'Edit %r for %s' % (depl.name, project['name'])
    return render_template("edit.html", form=form, action=action,
                           project=project, backlink=backlink,
                           form_action=form_action % (project_id, depl.id))
