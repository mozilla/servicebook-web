from flask import render_template, Blueprint


frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def home():
    projects = frontend.app.db.get_entries('project', sort='name')
    return render_template('home.html', projects=projects)


@frontend.route("/info")
def info():
    projects = frontend.app.db.get_entries('project', sort='name')
    return render_template('info.html', projects=projects)


@frontend.route("/coverage")
def coverage():
    projects = frontend.app.db.get_entries('project', sort='name')
    return render_template('coverage.html', projects=projects)
