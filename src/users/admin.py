from django.contrib import admin
from django.contrib.auth.models import User

from .models import DiscordUser

@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    search_fields = ['username']
