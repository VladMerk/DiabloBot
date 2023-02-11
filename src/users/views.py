from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import TemplateView
from social.models import Social
import requests


class HomeView(TemplateView):
    template_name = "users/home.html"

def discord_login(request):
    """Функция вызываемая при переходе по ссылке авторизации через дискорд.
    Осуществляется редирект на сайт дискорда для получения токена.
    После подтверждения авторизации по дискорду, с сайта дискорда осуществляется
    переход на сслыку, указанную в настройках дискорда.
    В данном случае - /users/login/redirect/
    """
    link = Social.objects.get(name="Discord").auth_url
    return redirect(link)


def discord_login_redirect(request):
    """
    Функция вызывается после перехода с сайта дискорда.
    Содержит в теле сслыки - code - необходимый для подтверждения
    """
    # получаем код из ссылки после перехода
    code = request.GET.get("code")
    # полученный код отправляется опять на сервер дискорда
    # для проверки и обратно получаем данные юзера для аутентификации
    user = _exchange_code(code)
    print(type(user))
    # если юзер получен пробуем его авторизовать на сайте
    discord_user = authenticate(request=request, user=user)
    # потом залогинить
    login(request, user=discord_user)
    # если залогинили, тогда переводим на главную страницу юзера
    return redirect(reverse("users:users_home"))


def _exchange_code(code):
    client = list(Social.objects.values("client_id", "client_secret")).pop()
    data = {
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/users/login/redirect/",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.Session().post(
        url="https://discord.com/api/oauth2/token", data=data, headers=headers
    )
    credentials = response.json()
    access_token = credentials.get("access_token")
    response = requests.get(
        url="https://discord.com/api/v10/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return response.json()
