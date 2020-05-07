from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Public is one that is not authenticated"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is success"""
        payload = {
            'email': 'test@ukraine.gov',
            'password': 'test123',
            'name': 'johngalt'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_duplicate_user(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@ukraine.gov', 'password': 'testPass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error_returned(self):
        """
        Test that error response returned if
        password is fewer than 5 chars
        """
        invalid_short_password = 'pass'
        payload = {'email': 'test@ukraine.gov',
                   'name': 'test',
                   'password': invalid_short_password}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_user_not_created(self):
        """
        Test that user is not created if
        password is fewer than 5 chars
        """
        invalid_short_password = 'pass'
        payload = {'email': 'test@ukraine.gov',
                   'name': 'test',
                   'password': invalid_short_password}
        self.client.post(CREATE_USER_URL, payload)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
