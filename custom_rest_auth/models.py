from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token


class ExpiringToken(Token):
    class Meta:
        proxy = True

    @property
    def is_expired(self):
        return timezone.now() >= self.created + settings.USER_TOKEN_LIFETIME
