from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Settings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    terror_channel = models.ForeignKey(
        "guilds.Channels",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terror_set",
    )
    clone_channel = models.ForeignKey(
        "guilds.Channels",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clone_set",
    )
    max_time = models.PositiveIntegerField(default=5, validators=[MinValueValidator(5), MaxValueValidator(60)])
    fasttrade_channel = models.ForeignKey(
        "guilds.Channels",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fasttrade_set",
    )
    fasttrade_channel_role = models.ForeignKey("guilds.Roles", blank=True, null=True, on_delete=models.SET_NULL)
    fasttrade_channel_time = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"


class Channels(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Channels"
        verbose_name_plural = "Channels"
        ordering = ["name"]


class Roles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Roles"
        verbose_name_plural = "Roles"
        ordering = ["name"]


class TerrorZones(models.Model):
    key = models.CharField(max_length=255, primary_key=True, unique=True)
    name_en = models.CharField(max_length=150, blank=True, null=True)
    name_ru = models.CharField(max_length=150, blank=True, null=True)
    act = models.CharField(max_length=5, blank=True, null=True)
    immunities_en = models.TextField(blank=True, null=True)
    immunities_ru = models.TextField(blank=True, null=True)
    boss_packs = models.CharField(max_length=25, blank=True, null=True)
    super_uniques = models.CharField(max_length=200, blank=True, null=True)
    sparkly_chests = models.PositiveIntegerField(blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Terror Zones"
        verbose_name_plural = "Terror Zones"
        ordering = ("act", "name_en")
