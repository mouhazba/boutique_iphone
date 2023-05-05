from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from app.views import login_user


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_successful(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'testpass'})
        request.user = self.user
        response = login_user(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

    def test_login_failed(self):
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'wrongpass'})
        request.user = self.user
        response = login_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Données invalides')
