# Generated by Django 4.1.6 on 2023-02-16 22:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guilds", "0006_settings_fasttrade_channel_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="terrorzones",
            name="sparkly_chests",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
