from rest_framework.authtoken.views import obtain_auth_token
from .views import registration, logout_view
from django.urls import path

urlpatterns = [
    path("login/", obtain_auth_token, name='profile-login'),
    path("logout/", logout_view, name='profile-logout'),
    path("registration/", registration, name='profile-registration'),
]
