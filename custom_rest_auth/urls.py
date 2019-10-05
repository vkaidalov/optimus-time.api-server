from django.urls import path

from . import views

urlpatterns = [
    path('hello-world/', views.HelloWorldView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
    path('auth/register/', views.RegisterView.as_view()),
]
