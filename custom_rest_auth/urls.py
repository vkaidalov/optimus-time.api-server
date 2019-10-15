from django.urls import path

from . import views

urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='auth-login'),
    path('auth/logout/', views.LogoutView.as_view(), name='auth-logout'),
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    path('auth/password/change/', views.PasswordChangeView.as_view(), name='auth-password-change'),
    path('auth/profile/', views.UserProfileView.as_view(), name='auth-profile'),
]
