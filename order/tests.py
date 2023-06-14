from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from django.contrib.auth.models import User
from django.contrib.auth import get_user
from order.views import user_login, user_create

def setup_request(request):
    middleware = SessionMiddleware(request)
    middleware.process_request(request)
    request.session.save()

    return request

class UserAuthTests(TestCase):
    def setUp(self):
        password = "password"
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username="test1", email="test1@example.com", password=password)
        self.user1.raw_password = password

    def test_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        resp = self.client.post('/login/', {'username': self.user1.username, 'password': self.user1.raw_password})
        
        self.assertTrue("login_error" not in resp.client.session.keys())
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_failed_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        resp = self.client.post('/login/', {'username': self.user1.username, 'password': 'wrong'})
        
        self.assertTrue("login_error" in resp.client.session.keys())
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_create_account(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        username = "test2"
        email = "test2@example.com"
        password = "password"

        resp = self.client.post('/create-account/', {'username': username, 'email': email, 'password': password})
        
        new_user = get_user(self.client)
        self.assertEqual(len(resp.client.session["account_create_errors"]), 0)
        self.assertTrue(new_user.is_authenticated)
        self.assertEqual(new_user.username, username)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))

    def test_duplicate_username_create_account(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        username = "test1"
        email = "test2@example.com"
        password = "password"

        resp = self.client.post('/create-account/', {'username': username, 'email': email, 'password': password})
        
        new_user = get_user(self.client)
        self.assertEqual(len(resp.client.session["account_create_errors"]), 1)
        self.assertFalse(new_user.is_authenticated)

    def test_duplicate_username_create_account(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        username = "test2"
        email = "test1@example.com"
        password = "password"

        resp = self.client.post('/create-account/', {'username': username, 'email': email, 'password': password})
        
        new_user = get_user(self.client)
        self.assertEqual(len(resp.client.session["account_create_errors"]), 1)
        self.assertFalse(new_user.is_authenticated)


