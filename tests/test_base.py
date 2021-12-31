from flask.helpers import url_for
from flask_testing import TestCase
from flask import current_app
from werkzeug.wrappers import response

from main import app

class TestBase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app


    def test_app_exists(self):
        self.assertIsNotNone(current_app)


    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])


    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))


    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)


    def test_hello_post(self):
        
        # response = self.client.post(url_for('hello'), data=fake_form)
        # self.assertRedirects(response, url_for('index'))

        response = self.client.post(url_for('hello'))
        self.assertTrue(response.status_code, 405)
        
    
    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)


    def test_auth_login_template(self):
        response = self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')


    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fakePassword'
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))