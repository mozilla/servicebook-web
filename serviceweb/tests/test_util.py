from werkzeug.exceptions import Forbidden
from flask import request
from serviceweb.tests.support import BaseTest
from serviceweb.util import safe_redirect


class UtilTest(BaseTest):

    def test_some_internal(self):
        with self.app.app.test_request_context():
            res = safe_redirect('/')
            self.assertEqual(res.location, '/')

            res = safe_redirect('/user/1')
            self.assertEqual(res.location, '/user/1')

            self.assertRaises(Forbidden, safe_redirect,
                              'http://localhost:67/user/1')

            url = request.host_url + '/user/1'
            res = safe_redirect(url)
            self.assertEqual(res.location, url)

    def test_forbidden(self):
        with self.app.app.test_request_context():
            self.assertRaises(Forbidden, safe_redirect, 'http://someothersite')
