from django.urls import path

from .views import HelloWorldView, LoginView

urlpatterns = [
    path('hello-world/', HelloWorldView.as_view()),
    path('auth/login/', LoginView.as_view()),
]
