from django.db import models


class Guild(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, null=True, blank=True
    )
    terror_channels = models.ForeignKey(
        "guilds.Channel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terror_set",
    )
    fasttrade_channels = models.ForeignKey(
        "guilds.Channel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fasttrade_set",
    )

    def __str__(self):
        return self.name


class Channel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.guild.name}"


class Roles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TerrorZoneTemplate(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    name_en = models.CharField(max_length=150, blank=True, null=True)
    name_ru = models.CharField(max_length=150, blank=True, null=True)
    act = models.CharField(max_length=5, blank=True, null=True)
    immunities_en = models.TextField(blank=True, null=True)
    immunities_ru = models.TextField(blank=True, null=True)
    boss_packs = models.CharField(max_length=25, blank=True, null=True)
    super_uniques = models.CharField(max_length=200, blank=True, null=True)
    sparkly_chests = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Terror Zone Template"
        ordering = ('act', 'name_en')


class TerrorZones(models.Model):
    zone = models.OneToOneField(TerrorZoneTemplate, on_delete=models.CASCADE, unique=True, related_name='zones')
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, blank=True, null=True)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.zone)

    class Meta:
        verbose_name = 'TerrorZones'
        verbose_name_plural = 'TerrorZones'
        ordering = ('zone__act', 'zone')
