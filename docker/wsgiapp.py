import site
import sys
import os
import codecs
from werkzeug.wsgi import DispatcherMiddleware
from serviceweb.server import create_app
from servicebook.server import create_app as create_api


ini = os.path.join(os.path.dirname(__file__), 'serviceweb.ini')
application = create_app(ini_file=ini)
wsgi = application.wsgi_app
api = create_api(ini_file=ini)
application.wsgi_app = DispatcherMiddleware(wsgi, {'/api': api.wsgi_app})


if __name__ == "__main__":
    application.run(host='0.0.0.0')
