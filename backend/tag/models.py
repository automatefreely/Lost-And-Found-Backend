from django.db import models

# Create your models here.
class Tag(models.Model):
    id=models.CharField("Unique ID of tag",max_length=16,primary_key=True)
    name=models.CharField("Tag name",max_length=32)
    img=models.CharField("tag image",max_length=300)