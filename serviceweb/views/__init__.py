from .users import users_bp
from .projects import projects
from .auth import auth
from .frontend import frontend
from .groups import groups
from .edit import edit
from .heartbeat import heartbeat


blueprints = (users_bp, projects, auth, frontend, groups, edit,
              heartbeat)
