from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ExpiringToken

USER_MODEL = get_user_model()

VALID_USERNAME = 'hesoyam11'
VALID_PASSWORD = 'postgres'


class LoginViewTests(APITestCase):
    LOGIN_URL = reverse('auth-login')

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            username=VALID_USERNAME, password=VALID_PASSWORD
        )

    def test_login_with_valid_data(self):
        data = {
            'username': VALID_USERNAME, 'password': VALID_PASSWORD
        }
        response = self.client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = ExpiringToken.objects.get(key=response.data.get('token'))
        self.assertEqual(token.is_expired, False)
        logged_in_user = token.user
        self.assertEqual(logged_in_user.username, self.user.username)

    def test_login_with_invalid_username(self):
        data = {
            'username': 'aezakme111', 'password': 'postgres'
        }
        response = self.client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_with_invalid_password(self):
        data = {
            'username': VALID_USERNAME, 'password': 'postgres_s_s_s'
        }
        response = self.client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LogoutViewTests(APITestCase):
    LOGOUT_URL = reverse('auth-logout')

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            username=VALID_USERNAME, password=VALID_PASSWORD
        )

    def test_logout(self):
        token = ExpiringToken.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}'
        )
        response = self.client.post(self.LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            ExpiringToken.objects.filter(key=token.key), []
        )
