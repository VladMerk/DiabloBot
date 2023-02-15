from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import DiscordManager
from . import utils


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    discriminator = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, null=True)
    avatar = models.CharField(max_length=150, blank=True, null=True)
    locale = models.CharField(max_length=50, blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    messages = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    cookies = models.PositiveIntegerField(default=0)

    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = DiscordManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}#{self.discriminator}" if self.discriminator else self.username

    def save(self, *args, **kwargs):
        self.level = utils.get_level(self.messages)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["level", "username"]
