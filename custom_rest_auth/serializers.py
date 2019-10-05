from rest_framework import serializers
from rest_framework.authtoken.models import Token


USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 150

PASSWORD_MIN_LENGTH = 8


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        required=True
    )
    password = serializers.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        required=True
    )


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
