from .users import users_bp
from .actions import actions
from .projects import projects
from .auth import auth
from .frontend import frontend
from .groups import groups
from .edit import edit


blueprints = (users_bp, actions, projects, auth, frontend, groups, edit)
