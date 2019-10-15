from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APITestCase

from .authentication import ExpiringTokenAuthentication
from .models import ExpiringToken

USER_MODEL = get_user_model()


class ExpiringTokenAuthenticationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            username='hesoyam11', password='postgres'
        )

    def test_with_not_expired_token(self):
        not_expired_token = ExpiringToken.objects.create(user=self.user)
        self.assertEqual(not_expired_token.is_expired, False)
        authentication = ExpiringTokenAuthentication()
        user, token = authentication.authenticate_credentials(
            not_expired_token.key
        )
        self.assertEqual(user, not_expired_token.user)
        self.assertEqual(token, not_expired_token)

    def test_with_expired_token(self):
        expired_token = ExpiringToken.objects.create(user=self.user)
        expired_token.created -= settings.USER_TOKEN_LIFETIME
        expired_token.save()
        self.assertEqual(expired_token.is_expired, True)

        authentication = ExpiringTokenAuthentication()
        with self.assertRaises(AuthenticationFailed):
            authentication.authenticate_credentials(expired_token.key)
