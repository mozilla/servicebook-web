from flask import render_template, Blueprint, request
from serviceweb.search import search_data


frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def home():
    search = request.args.get('search')
    if search:
        search_results = search_data(search)
        searched = True
    else:
        search_results = []
        searched = False
    projects = frontend.app.db.get_entries('project', sort='name')

    return render_template('home.html', projects=projects,
                           search_results=search_results,
                           searched=searched)


@frontend.route("/info")
def info():
    projects = frontend.app.db.get_entries('project', sort='name')
    return render_template('info.html', projects=projects)


@frontend.route("/coverage")
def coverage():
    projects = frontend.app.db.get_entries('project', sort='name')
    return render_template('coverage.html', projects=projects)
