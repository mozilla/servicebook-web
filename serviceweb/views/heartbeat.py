import os
from flask import Blueprint, jsonify, g, Response


here = os.path.abspath(os.path.dirname(__file__))
heartbeat = Blueprint('heartbeat', __name__)


@heartbeat.route('/__version__')
def _version():
    with open(os.path.join(here, '..', 'templates', 'version.json')) as f:
        return Response(f.read(), mimetype='application/json')


@heartbeat.route('/__lbheartbeat__')
def _lbheartbeat():
    return ''


@heartbeat.route('/__heartbeat__')
def _heartbeat():
    results = {}
    try:
        users = g.db.get_entries('user')
        results['database'] = len(users) > 0
    except Exception:
        results['database'] = False
    return jsonify(results)
