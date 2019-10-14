from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import ExpiringToken


USER_MODEL = get_user_model()


class ExpiringTokenModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            username='hesoyam', password='postgres'
        )

    def test_is_expired_with_new_token(self):
        expiring_token = ExpiringToken(user=self.user)
        expiring_token.save()
        self.assertIs(expiring_token.is_expired, False)

    def test_is_expired_with_expired_token(self):
        expired_token = ExpiringToken(user=self.user)
        expired_token.save()
        expired_token.created -= settings.USER_TOKEN_LIFETIME
        expired_token.save()
        self.assertIs(expired_token.is_expired, True)
