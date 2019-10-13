from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import ExpiringToken


USER_MODEL = get_user_model()


class ExpiringTokenModelTests(TestCase):
    def test_is_expired_with_new_token(self):
        user = USER_MODEL.objects.create_user(
            username='hesoyam', password='postgres'
        )

        expiring_token = ExpiringToken(user=user)
        expiring_token.save()
        self.assertFalse(expiring_token.is_expired())
