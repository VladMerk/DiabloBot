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
                "fields": ("bot", "joined_at", "removed_at"),
            }
        ),
        (
            " ",
            {
                "fields": ("roles",),
            }
        ),
    )
    search_fields = ['id', 'username']
    readonly_fields = ['id', 'username', 'discriminator', 'bot', 'roles', 'joined_at', 'removed_at']
    list_display = ("username", "joined_at")
    list_filter = ("joined_at",)
    ordering = ("-joined_at",)
