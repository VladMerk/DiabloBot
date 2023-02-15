from django.contrib import admin

from .models import (Channel,
                    Guild,
                    Roles,
                    TerrorZoneTemplate,
                    TerrorZones,
                )

admin.site.register(Guild)
admin.site.register(Roles)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_filter = ('guild',)
    list_display =  ('name', 'guild')


@admin.register(TerrorZoneTemplate)
class TerrorZoneTemplatesAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'act')
    list_filter = ('act',)

@admin.register(TerrorZones)
class TerrorZonesAdmin(admin.ModelAdmin):
    list_display = ('zone', 'guild')
    list_filter = ( 'zone__act', 'guild')
