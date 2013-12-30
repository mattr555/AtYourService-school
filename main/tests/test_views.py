from django.test import TestCase

from .test_models import create_test_user

class NavbarTest(TestCase):
    def setUp(self):
        create_test_user('test1')
        
    def test_navbar_no_user(self):
        response = self.client.get('/')
        self.assertContains(response, 'Not logged in.')

    def test_navbar_user_logged_in(self):
        self.client.login(username='test1', password='test1')
        response = self.client.get('/')
        self.assertContains(response, 'Logged in as')
        self.assertContains(response, 'test1')