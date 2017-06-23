import random
import yaml
import requests

from flask import render_template, abort, request, g, Blueprint

from serviceweb.auth import only_for_editors
from serviceweb.forms import NewProjectForm, DeploymentForm
from serviceweb.util import add_view, safe_redirect
from serviceweb.screenshots import get_list
from restjson.client import objdict


projects = Blueprint('projects', __name__)


_STATUSES = 'status=NEW&status=REOPENED&status=UNCONFIRMED&status=ASSIGNED'
_BUGZILLA = ('https://bugzilla.mozilla.org/rest/bug?' + _STATUSES +
             '&product=%s&component=%s&limit=10')


@projects.route("/project", methods=['GET', 'POST'])
@only_for_editors
def add_project():
    return add_view(NewProjectForm, 'project', 'Add a new project',
                    '/project', '/project')


def get_last_builds(job_name):
    # just random samples for now
    url = 'https://webqa-ci.mozilla.com/job/mozillians.prod/%d/'
    return [{'url': url % (i + 100),
             'fullDisplayName': 'mozillians.prod #%d' % (i + 100),
             'result': random.choice(['SUCCESS', 'FAILURE'])}
            for i in range(10)]


@projects.route("/project/<int:project_id>")
def project(project_id):
    project = g.db.get_entry('project', project_id)
    if not project.public and not g.user_in_mozteam:
        return abort(404)

    # scraping jenkins info
    # for job in project['jenkins_jobs']:
    #    builds.extend(get_last_builds(job['id']))
    builds = None    # get_last_builds('blah')

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
        try:
            res = requests.get(swagger)
            if res.status_code == 200:
                project_info = yaml.load(res.content)['info']
        except Exception:
            # XXX log it
            pass

    backlink = '/'
    edit = '/project/%d/edit' % project_id
    screenshots = ['https://s3-us-west-2.amazonaws.com/servicebook/' + key
                   for key in get_list(project_id)]
    return render_template('project.html', project=project, bugs=bugs,
                           edit=edit, jenkins_builds=builds,
                           project_info=project_info, backlink=backlink,
                           screenshots=screenshots)


@projects.route("/project/<int:project_id>/deployments",
                methods=['GET', 'POST'])
@only_for_editors
def add_deployment(project_id):
    form = DeploymentForm(request.form)
    project = g.db.get_entry('project', project_id)

    if request.method == 'POST' and form.validate():
        deployment = objdict({'project_id': project_id})
        form.populate_obj(deployment)
        g.db.create_entry('deployment', deployment)
        return safe_redirect('/project/%d' % project_id)

    action = 'Add a new deployment for %s' % project.name
    return render_template("edit.html", form=form, action=action,
                           form_action="/project/%s/deployments" % project_id)


@projects.route("/project/<int:project_id>/deployments/<int:depl_id>/delete",
                methods=['GET'])
@only_for_editors
def remove_deployment(project_id, depl_id):
    g.db.delete_entry('deployment', depl_id)
    return safe_redirect('/project/%d' % (project_id))


@projects.route("/project/<int:project_id>/deployments/<int:depl_id>/edit",
                methods=['GET', 'POST'])
@only_for_editors
def edit_deployment(project_id, depl_id):
    depl = g.db.get_entry('deployment', depl_id)
    project = depl.project
    form = DeploymentForm(request.form, depl)

    if request.method == 'POST' and form.validate():
        form.populate_obj(depl)
        g.db.update_entry('deployment', depl)
        return safe_redirect('/project/%d' % (project_id))

    form_action = '/project/%d/deployments/%d/edit'
    backlink = '/project/%d' % project_id
    action = 'Edit %r for %s' % (depl.name, project['name'])
    return render_template("edit.html", form=form, action=action,
                           project=project, backlink=backlink,
                           form_action=form_action % (project_id, depl.id))
