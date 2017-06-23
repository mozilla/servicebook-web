from flask import redirect, Blueprint, request
from flask import render_template

from serviceweb.auth import only_for_editors
from serviceweb.forms import get_form
from serviceweb.screenshots import upload_file


upload = Blueprint('upload', __name__)


@upload.route("/project/<int:project_id>/upload",
              methods=['POST', 'GET'])
@only_for_editors
def _upload_screenshot(project_id):
    backlink = "/project/%d" % project_id
    if request.method == 'POST':
        data_file = request.files.get('file')
        file_name = data_file.filename
        upload_file(project_id, file_name, data_file)
        return redirect(backlink)
    else:
        form = get_form('upload')(request.form)
        action = "Upload screenshot"
        return render_template("edit.html", form=form, action=action,
                               backlink=backlink, form_id='upload')
