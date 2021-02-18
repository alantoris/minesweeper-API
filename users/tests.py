# Django
from django.conf import settings
from django.test import TestCase

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


#Models
from django.contrib.auth.models import User

class UserSignUpSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_signup_ok(self):
        response = self.client.post(
            '/users/signup/', 
            {
                'email': 'mail@example.com',
                'username': 'example',
                'password': 'pwd1234**',
                'password_confirmation':  'pwd1234**'
            },
            format='json')
        self.assertEquals(201, response.status_code)
    
    def test_signup_password_common(self):
        response = self.client.post(
            '/users/signup/', 
            {
                'email': 'mail@example.com',
                'username': 'example',
                'password': 'password1234',
                'password_confirmation':  'password1234'
            },
            format='json')
        self.assertEquals(400, response.status_code)
        self.assertEquals({'non_field_errors': ['This password is too common.']},
                          response.data)

class UserLoginSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "user_example"
        self.password = "user_password"
    
    def test_signup_and_login_ok(self):
        response = self.client.post(
            '/users/signup/', 
            {
                'email': 'mail@example.com',
                'username': self.username,
                'password': self.password,
                'password_confirmation':  self.password
            },
            format='json')
        self.assertEquals(201, response.status_code)
        response = self.client.post(
            '/users/login/', 
            {
                'username': self.username,
                'password': self.password
            },
            format='json')
        self.assertEquals(201, response.status_code)
    
    def test_login_error(self):
        response = self.client.post(
            '/users/signup/', 
            {
                'email': 'mail2@example.com',
                'username': self.username,
                'password': self.password,
                'password_confirmation':  self.password
            },
            format='json')
        self.assertEquals(201, response.status_code)
        response = self.client.post(
            '/users/login/', 
            {
                'username': self.username,
                'password': 'incorrect_password',
            },
            format='json')
        self.assertEquals(400, response.status_code)
        self.assertEquals({'non_field_errors': ['Invalid credentials']},
                          response.data)



