# Generated by Django 4.1.6 on 2023-07-27 05:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guilds", "0004_alter_roles_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channels",
            name="name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterUniqueTogether(
            name="channels",
            unique_together={("id", "name")},
        ),
    ]