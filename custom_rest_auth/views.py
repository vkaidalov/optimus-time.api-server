from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from . import serializers


class HelloWorldView(APIView):
    def get(self, _request):
        return Response({
            'message': 'Hello World!'
        })


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        login_serializer = serializers.LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(**login_serializer.validated_data)

        if not user:
            raise exceptions.NotFound('Invalid username/password.')

        token, _created = Token.objects.get_or_create(user=user)

        if timezone.now() >= token.created + settings.USER_TOKEN_LIFETIME:
            token.delete()
            token = Token.objects.create(user=user)

        token_serializer = serializers.TokenSerializer(token)
        return Response(token_serializer.data)


class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response({'detail': 'Successfully logged out.'})


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Registration completed.'})


class PasswordChangeView(APIView):
    serializer_class = serializers.PasswordChangeSerializer

    def post(self, request):
        serializer = serializers.PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            raise ValidationError({
                'old_password': ['Wrong password.']
            })

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password changed.'})


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return get_user_model().objects.none()
