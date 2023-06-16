from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from django.contrib.auth.models import User
from django.contrib.auth import get_user
from order.models import Store, BusinessHours, Address, OrderMethod, OrderMethods
from order.views import user_login, user_create

from datetime import time

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

    def test_duplicate_email_create_account(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        username = "test2"
        email = "test1@example.com"
        password = "password"

        resp = self.client.post('/create-account/', {'username': username, 'email': email, 'password': password})
        
        new_user = get_user(self.client)
        self.assertEqual(len(resp.client.session["account_create_errors"]), 1)
        self.assertFalse(new_user.is_authenticated)

    def test_duplicate_username_by_case_create_account(self):
            self.assertFalse(get_user(self.client).is_authenticated)

            username = "Test1"
            email = "test1@example.com"
            password = "password"

            resp = self.client.post('/create-account/', {'username': username, 'email': email, 'password': password})
            
            new_user = get_user(self.client)
            self.assertEqual(len(resp.client.session["account_create_errors"]), 1)
            self.assertFalse(new_user.is_authenticated)

    def test_duplicate_email_by_case_create_account(self):
        self.assertFalse(get_user(self.client).is_authenticated)

        username = "test2"
        email = "Test1@example.com"
        password = "password"

        resp = self.client.post('/create-account/', {'username': username, 'email': email, 'password': password})
        
        new_user = get_user(self.client)
        self.assertEqual(len(resp.client.session["account_create_errors"]), 1)
        self.assertFalse(new_user.is_authenticated)


class StoreSelectionTests(TestCase):
    def setUp(self):
        username = "test1"
        password = "password"
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username=username, email="test1@example.com", password=password)
        self.client.login(username=username, password=password)

        self.address1 = Address.objects.create(street="123 test street", city="tempcity", state="NA", zipcode="12345")
        self.schedule1 = BusinessHours.objects.create(mon_open=time(9, 30), mon_close=time(21, 30))
        self.store1 = Store.objects.create(name="test store 1", address=self.address1, timezone="US/Mountain", schedule=self.schedule1)

        self.address2 = Address.objects.create(street="123 example ave", city="exampleton", state="PA", zipcode="67891")
        self.schedule2 = BusinessHours.objects.create()
        self.store2 = Store.objects.create(name="test store 2", address=self.address2, timezone="US/Mountain", schedule=self.schedule2)

    def test_store_processing(self):
        resp = self.client.get('/store-selection/')
        processed_stores = resp.context[0].dicts[3]['stores']

        self.assertEqual(len(processed_stores), 2)
    
    def test_store_oos_closed(self):
        self.store1.out_of_schedule_close = True

        resp = self.client.get('/store-selection/')
        processed_store1 = resp.context[0].dicts[3]['stores'][0]

        self.assertFalse(processed_store1['is_open'])

    def test_store_all_days_closed(self): # Store 2 is closed all days
        resp = self.client.get('/store-selection/')
        processed_store2 = resp.context[0].dicts[3]['stores'][1]

        self.assertFalse(processed_store2['is_open'])



