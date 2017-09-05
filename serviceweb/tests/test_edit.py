from webtest.app import AppError
from serviceweb.tests.support import BaseTest


class EditTest(BaseTest):
    def test_edit_project(self):
        # first attempt fails since we're not logged in
        self.assertRaises(AppError, self.app.get, '/project/1/edit')

        # now logging in
        with self.logged_in():
            project = self.app.get('/project/1/edit')
            form = project.forms[0]
            old_name = form['name'].value
            form['name'] = 'new name'
            form.submit()

            # let's check it changed
            self.assertTrue(b'new name' in self.app.get('/project/1').body)

            # change it back to the old value
            project = self.app.get('/project/1/edit')
            form = project.forms[0]
            form['name'] = old_name
            form.submit()

    def test_edit_user(self):
        with self.logged_in():
            user = self.app.get('/user/1/edit')
            form = user.forms[0]
            old_name = form['firstname'].value
            form['firstname'] = 'new name'
            form.submit()

            # let's check it changed
            self.assertTrue(b'New name' in self.app.get('/user/1').body)

            # change it back to the old value
            user = self.app.get('/user/1/edit')
            form = user.forms[0]
            form['firstname'] = old_name
            form.submit()

            # let's control we don't have a dupe
            users = self.app.get('/user')
            tds = users.html.find_all('td')
            self.assertEqual(len([td.text for td in tds
                                  if td.text == old_name]), 1)

    def test_delete_user(self):
        with self.logged_in():
            deleted = self.app.get('/user/1/delete')
            self.assertEqual(deleted.status_code, 302)
            res = self.app.get('/user/1/delete', status=404)
            self.assertTrue(b'Error 404' in res.body)
            res = self.app.get('/user/1', status=404)
            self.assertTrue(b'Error 404' in res.body)

    def test_add_user(self):
        with self.logged_in():
            user = self.app.get('/adduser')
            form = user.forms[0]
            form['firstname'] = 'Joe'
            form['lastname'] = 'Doe'
            res = form.submit().follow()

            # let's check it changed
            self.assertTrue(b'Joe' in res.body)

    def test_add_relation(self):
        with self.logged_in():
            url = ('/project/1/add_relation/tests/project_test?'
                   'inline=1&relation=project_id')

            rel = self.app.get(url)
            new_rel = rel.forms[1]
            new_rel['name'] = 'blah'
            next_step = new_rel.submit()
            self.assertTrue(next_step.location.endswith('/project/1/edit'))

            # let's check it changed
            self.assertTrue(b'blah' in self.app.get('/project/1').body)
