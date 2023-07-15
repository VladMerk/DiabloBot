from django.contrib import admin
from django.contrib.auth.models import User

from .models import DiscordUser

admin.site.register(DiscordUser)
