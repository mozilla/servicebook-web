import warnings
import shutil
import os
from unittest import TestCase
import multiprocessing
from contextlib import contextmanager
import json
import re
import time
from http.client import HTTPConnection
import signal

import yaml
import requests_mock
from flask_webtest import TestApp
from serviceweb.server import create_app


_ONE_TIME = None
_INI = os.path.join(os.path.dirname(__file__), 'serviceweb.ini')
_BOOK = os.path.join(os.path.dirname(__file__), 'servicebook.ini')
_DB = os.path.join(os.path.dirname(__file__), 'projects.db')


def run_server(port=8888):
    """Running in a subprocess to avoid any interference
    """
    def _run():
        import os
        from servicebook.server import create_app
        import socketserver
        import sys
        from io import StringIO
        import warnings

        # might want to drop it in a file
        sys.stderr = sys.stdout = StringIO()
        socketserver.TCPServer.allow_reuse_address = True

        test_dir = os.path.dirname(_BOOK)
        os.chdir(test_dir)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            app = create_app(_BOOK)
            try:
                app.run(port=port, debug=False)
            except KeyboardInterrupt:
                pass

    p = multiprocessing.Process(target=_run)
    p.start()
    start = time.time()
    connected = False

    while time.time() - start < 5 and not connected:
        try:
            conn = HTTPConnection('localhost', 8888)
            conn.request("GET", "/api/")
            conn.getresponse()
            connected = True
        except Exception:
            time.sleep(.1)

    if not connected:
        os.kill(p.pid, signal.SIGTERM)
        p.join(timeout=1.)
        raise OSError('Could not connect to coserver')
    return p


class BaseTest(TestCase):
    def setUp(self):
        super(BaseTest, self).setUp()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            global _ONE_TIME
            if _ONE_TIME is None:
                _ONE_TIME = TestApp(create_app(_INI))
            shutil.copyfile(_DB, _DB + '.saved')
            self._coserver = run_server(8888)
            self.app = _ONE_TIME

    def tearDown(self):
        os.kill(self._coserver.pid, signal.SIGTERM)
        shutil.copyfile(_DB + '.saved', _DB)
        self._coserver.join(timeout=1.)
        super(BaseTest, self).tearDown()

    @contextmanager
    def logged_in(self, extra_mocks=None):
        if extra_mocks is None:
            extra_mocks = []

        # let's log in
        self.app.get('/login')
        # redirects to github, let's fake the callback
        code = 'yeah'
        github_resp = 'access_token=yup'
        github_user = {'login': 'tarekziade', 'name': 'Tarek Ziade'}
        github_matcher = re.compile('github.com/')
        github_usermatcher = re.compile('https://api.github.com/user')
        bz_matcher = re.compile('.*bugzilla.*')
        bz_resp = {'bugs': []}
        sw_matcher = re.compile('search.stage.mozaws.net.*')

        yamlf = os.path.join(os.path.dirname(__file__), '__api__.yaml')
        with open(yamlf) as f:
            sw_resp = yaml.load(f.read())

        headers = {'Content-Type': 'application/json'}
        with requests_mock.Mocker(real_http=True) as m:
            m.post(github_matcher, text=github_resp)
            m.get(github_usermatcher, json=github_user)
            m.get(bz_matcher, text=json.dumps(bz_resp))
            m.get(sw_matcher, text=json.dumps(sw_resp))
            self.app.get('/github/callback?code=%s' % code)
            for verb, url, text in extra_mocks:
                m.register_uri(verb, re.compile(url), text=text,
                               headers=headers)

            # at this point we are logged in
            try:
                yield
            finally:
                # logging out
                self.app.get('/logout')
