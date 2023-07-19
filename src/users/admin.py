from django.contrib import admin
from django.contrib.auth.models import User

from .models import DiscordUser

@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            " ",
            {
                "fields": ("id", "username", "discriminator"),
            },
        ),
        (
            " ",
            {
                "fields": ("bot", "joined_at"),
            }
        ),
    )
    search_fields = ['username']
    readonly_fields = ['id', 'username', 'discriminator']
    list_display = ("username", "joined_at")
    list_filter = ("joined_at",)
    ordering = ("-joined_at",)
