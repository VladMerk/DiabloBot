from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from datetime import datetime



class DiscordUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    discriminator = models.CharField(max_length=50, blank=True)
    bot = models.BooleanField(blank=True, default=False)
    joined_at = models.DateTimeField(default=datetime(2000, 1, 1, 10, 0, 0))

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "DiscordUser"
        verbose_name_plural = "DiscordUsers"
        unique_together = [["id", "username"]]
