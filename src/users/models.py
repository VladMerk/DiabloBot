from django.db import models
from django.utils import timezone

from guilds.models import Roles


class DiscordUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=200)
    discriminator = models.CharField(max_length=50, blank=True)
    bot = models.BooleanField(blank=True, default=False)
    joined_at = models.DateTimeField(
        default=timezone.make_aware(timezone.datetime(2000, 1, 1, 10, 0, 0), timezone.get_current_timezone())
    )
    removed_at = models.DateTimeField(blank=True, null=True)
    roles = models.ManyToManyField(to=Roles)

    def __str__(self):
        return f"{self.username}#{self.discriminator}"

    class Meta:
        verbose_name = "DiscordUser"
        verbose_name_plural = "DiscordUsers"
        unique_together = [["username", "discriminator"]]
