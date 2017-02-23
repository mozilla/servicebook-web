from flask import g
from flask_nav import Nav, register_renderer
from flask_nav.elements import View, Navbar, Link
from flask_bootstrap.nav import BootstrapRenderer

from serviceweb.util import fullname


class RightNavbar(Navbar):
    pass


# XXX todo: allow the addition of navbar-right ul/li groups
class CustomRenderer(BootstrapRenderer):
    pass


class MyNav(Nav):
    def init_app(self, app):
        register_renderer(app, None, CustomRenderer)
        super(MyNav, self).init_app(app)


def build_nav():
    user = g.user
    elements = [View('Home', 'frontend.home'),
                View('Projects', 'frontend.info')]

    if user is None:
        link = Link('GitHub Login', '/login')
    else:
        elements.append(View('Manage Users', 'users.users_view'))
        name = fullname(user)
        elements.append(Link(name, '/user/%d' % user['id']))
        link = Link('Logout', '/logout')

    elements.append(link)

    return Navbar(*elements)


nav = MyNav()
nav.register_element('frontend_top', build_nav)
