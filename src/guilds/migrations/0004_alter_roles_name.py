# Generated by Django 4.1.6 on 2023-07-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guilds", "0003_alter_roles_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roles",
            name="name",
            field=models.CharField(max_length=150),
        ),
    ]
