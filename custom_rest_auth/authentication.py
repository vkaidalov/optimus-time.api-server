from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ExpiringToken


class ExpiringTokenAuthentication(TokenAuthentication):
    model = ExpiringToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        if token.is_expired:
            raise AuthenticationFailed(_("Token expired."))

        return user, token
