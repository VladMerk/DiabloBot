from django.contrib import admin

from .models import Channels, Roles, Settings, TerrorZones


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Name Server",
            {
                "fields": (
                    "id",
                    "name",
                ),
            },
        ),
        (
            "Terror Channel",
            {
                "fields": ("terror_channel", "max_time"),
            },
        ),
        (
            "Clone Channel",
            {
                "fields": ("clone_channel",),
            },
        ),
        (
            "Fast Trade Channel",
            {
                "fields": ("fasttrade_channel", "fasttrade_channel_role", "fasttrade_channel_time"),
            },
        ),
    )

    readonly_fields = ("id", "name")

    class Meta:
        verbose_name = "Settings"


@admin.register(TerrorZones)
class TerrorZonesAdmin(admin.ModelAdmin):
    list_display = (
        "act",
        "name_en",
    )
    list_filter = ("act",)
    list_display_links = ("name_en",)

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name')
    ordering = ['id']


@admin.register(Channels)
class ChannelsAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name')
