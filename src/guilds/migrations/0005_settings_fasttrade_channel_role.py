# Generated by Django 4.1.6 on 2023-02-16 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guilds", "0004_alter_settings_max_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="fasttrade_channel_role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="guilds.roles",
            ),
        ),
    ]