from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ExpiringToken

USER_MODEL = get_user_model()

VALID_USERNAME = 'hesoyam11'
VALID_EMAIL = 'hesoyam11@example.com'
VALID_PASSWORD = 'postgres'


class LoginViewTests(APITestCase):
    LOGIN_URL = reverse('auth-login')

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            username=VALID_USERNAME, password=VALID_PASSWORD
        )

    def test_login_with_valid_data(self):
        data = {'username': VALID_USERNAME, 'password': VALID_PASSWORD}
        response = self.client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = ExpiringToken.objects.get(key=response.data.get('token'))
        self.assertEqual(token.is_expired, False)
        logged_in_user = token.user
        self.assertEqual(logged_in_user.username, self.user.username)

    def test_login_with_expired_token(self):
        expired_token = ExpiringToken.objects.create(user=self.user)
        expired_token.created -= settings.USER_TOKEN_LIFETIME
        expired_token.save()
        self.assertEqual(expired_token.is_expired, True)
        data = {'username': VALID_USERNAME, 'password': VALID_PASSWORD}
        response = self.client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = ExpiringToken.objects.get(key=response.data.get('token'))
        self.assertEqual(token.user, self.user)

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


class RegisterViewTests(APITestCase):
    REGISTER_URL = reverse('auth-register')

    NEW_USERNAME = 'james_bond007'
    NEW_EMAIL = 'james_bond007@example.com'
    NEW_PASSWORD = 'postgres'

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            username=VALID_USERNAME, email=VALID_EMAIL, password=VALID_PASSWORD
        )

    def test_with_valid_data(self):
        data = {
            'username': self.NEW_USERNAME, 'email': self.NEW_EMAIL,
            'password': self.NEW_PASSWORD, 'passwordRepeat': self.NEW_PASSWORD
        }
        response = self.client.post(self.REGISTER_URL, data)
        self.assertEqual(response.status_code, 200)

    def test_with_not_unique_username_and_email(self):
        data = {
            'username': VALID_USERNAME, 'email': VALID_EMAIL,
            'password': self.NEW_PASSWORD, 'passwordRepeat': self.NEW_PASSWORD
        }
        response = self.client.post(self.REGISTER_URL, data)
        self.assertEqual(response.status_code, 400)

    def test_with_invalid_password_repeat(self):
        data = {
            'username': self.NEW_USERNAME, 'email': self.NEW_EMAIL,
            'password': self.NEW_PASSWORD, 'passwordRepeat': 'INVALID!!!'
        }
        response = self.client.post(self.REGISTER_URL, data)
        self.assertEqual(response.status_code, 400)


class PasswordChangeViewTests(APITestCase):
    PASSWORD_CHANGE_URL = reverse('auth-password-change')

    NEW_PASSWORD = 'very-strong-password'

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username=VALID_USERNAME, email=VALID_EMAIL, password=VALID_PASSWORD
        )

    def test_with_valid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.PASSWORD_CHANGE_URL, {
            'oldPassword': VALID_PASSWORD,
            'newPassword': self.NEW_PASSWORD,
            'newPasswordRepeat': self.NEW_PASSWORD,
        })
        self.assertEqual(response.status_code, 200)
        user = USER_MODEL.objects.get(pk=self.user.pk)
        self.assertEqual(user.check_password(self.NEW_PASSWORD), True)

    def test_with_invalid_password(self):
        self.client.force_login(self.user)
        response = self.client.post(self.PASSWORD_CHANGE_URL, {
            'oldPassword': 'INVALID!!!',
            'newPassword': self.NEW_PASSWORD,
            'newPasswordRepeat': self.NEW_PASSWORD,
        })
        self.assertEqual(response.status_code, 400)

    def test_with_invalid_repeat(self):
        self.client.force_login(self.user)
        response = self.client.post(self.PASSWORD_CHANGE_URL, {
            'oldPassword': VALID_PASSWORD,
            'newPassword': self.NEW_PASSWORD,
            'newPasswordRepeat': 'INVALID!!!',
        })
        self.assertEqual(response.status_code, 400)


class UserProfileViewTests(APITestCase):
    PROFILE_URL = reverse('auth-profile')

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username=VALID_USERNAME, email=VALID_EMAIL, password=VALID_PASSWORD
        )

    def test_get_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(self.PROFILE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('pk'), self.user.pk)
        self.assertEqual(response.data.get('username'), self.user.username)
        self.assertEqual(response.data.get('email'), self.user.email)
