from flask import render_template, Blueprint, request, g


frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def home():
    search = request.args.get('search')
    if search:
        search_results = g.search(search)['data']
        searched = True
    else:
        search_results = []
        searched = False

    projects = g.db.get_entries('project', sort='name')
    return render_template('home.html', projects=projects,
                           search_results=search_results,
                           searched=searched)


@frontend.route("/info")
def info():
    projects = g.db.get_entries('project', sort='name')
    return render_template('info.html', projects=projects)


@frontend.route("/coverage")
def coverage():
    projects = g.db.get_entries('project', sort='name')
    return render_template('coverage.html', projects=projects)
