from flask import render_template, Blueprint, request, g


frontend = Blueprint('frontend', __name__)


@frontend.route("/csp_report", methods=["POST"])
def csp_report():
    # XXX report CSP violations to sentry
    return ''


@frontend.route("/")
def home():
    search = request.args.get('search')
    if search:
        search_results = g.search(search)['data']
        if not g.user_in_mozteam:
            # let's filter out non public projects
            search_results = [proj for proj in search_results
                              if proj['public']]
        searched = True
    else:
        search_results = []
        searched = False

    projects = g.db.get_entries('project', sort='-last_modified')
    return render_template('home.html', projects=projects,
                           search_results=search_results,
                           searched=searched)


@frontend.route("/info")
def info():
    projects = g.db.get_entries('project', sort='-last_modified')
    return render_template('info.html', projects=projects)


@frontend.route("/coverage")
def coverage():
    projects = g.db.get_entries('project', sort='-last_modified')
    return render_template('coverage.html', projects=projects)
