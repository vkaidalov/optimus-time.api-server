from django.urls import path

from . import views

urlpatterns = [
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/password/change/', views.PasswordChangeView.as_view()),
    path('auth/profile/', views.UserProfileView.as_view()),
]
