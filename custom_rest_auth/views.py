from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    PasswordChangeSerializer,
    UserProfileSerializer
)
from .models import ExpiringToken


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(**login_serializer.validated_data)

        if not user:
            raise exceptions.NotFound('Invalid username/password.')

        token, _created = ExpiringToken.objects.get_or_create(user=user)

        if token.is_expired:
            token.delete()
            token = ExpiringToken.objects.create(user=user)

        return Response({'token': token.key})


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Successfully logged out.'})


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Registration completed.'})


class PasswordChangeView(APIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
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
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return get_user_model().objects.none()
