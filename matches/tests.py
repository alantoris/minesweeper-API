# Django
from django.conf import settings
from django.test import TestCase

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

#Models
from django.contrib.auth.models import User


def create_some_user():
    """Create a new user and token."""
    user = User.objects.create_user({
        "username": "username",
        "password": "password1234",
        "email": "example@gmail.com"
    })
            
    token, created = Token.objects.get_or_create(user=user)
    return user, token

class MatchViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user, token = create_some_user()
        self.token = token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_create_match_ok(self):
        response = self.client.post(
            '/matches/', 
            {
                'width': 25,
                'height': 25,
                'mines': 12
            },
            format='json')
        self.assertEquals(201, response.status_code)
    
    def test_big_match(self):
        response = self.client.post(
            '/matches/', 
            {
                'width': 250,
                'height': 25,
                'mines': 12
            },
            format='json')
        self.assertEquals(400, response.status_code)
        self.assertEquals({'width': ['Ensure this value is less than or equal to {}.'.format(settings.BOARD_MAX_WIDTH)]},
                          response.data)
    
    def test_param_required(self):
        response = self.client.post(
            '/matches/', 
            {
                'height': 25,
                'mines': 12
            },
            format='json')
        self.assertEquals(400, response.status_code)
        self.assertEquals({'width': ['This field is required.']},
                          response.data)

