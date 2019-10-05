from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, TokenSerializer


class HelloWorldView(APIView):
    def get(self, _request):
        return Response({
            'message': 'Hello World!'
        })


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=login_serializer.validated_data['username'],
            password=login_serializer.validated_data['password']
        )

        if not user:
            raise exceptions.NotFound('Invalid username/password.')

        token, _created = Token.objects.get_or_create(user=user)

        if timezone.now() >= token.created + settings.USER_TOKEN_LIFETIME:
            token.delete()
            token = Token.objects.create(user=user)

        token_serializer = TokenSerializer(token)
        return Response(token_serializer.data)
