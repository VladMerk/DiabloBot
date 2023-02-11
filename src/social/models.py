from django.db import models


class Social(models.Model):
    name = models.CharField(max_length=128)
    auth_url = models.CharField(max_length=255)
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)

    def __str__(self):
        return self.name
