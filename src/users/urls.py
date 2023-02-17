from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="users_home"),
    path("discord/login", views.discord_login, name="discord_login"),
    path("login/redirect/", views.discord_login_redirect, name="discord_login_redirect"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
