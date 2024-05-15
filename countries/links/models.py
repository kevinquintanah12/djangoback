from django.db import models
from django.conf import settings

from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    population = models.IntegerField()
    language = models.CharField(max_length=255)


    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.ForeignKey('links.Country', related_name='votes', on_delete=models.CASCADE)
