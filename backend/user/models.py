from django.contrib.postgres.fields import ArrayField
from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=50)
    