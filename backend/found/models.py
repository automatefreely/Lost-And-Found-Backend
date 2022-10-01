from django.db import models
from secrets import token_urlsafe

from ..user.models import User

# Create your models here.
class Found(models.Model):
    id = models.CharField("Unique ID of lost item", max_length=10, primary_key=True, default=token_urlsafe(10))
    user = models.ForeignKey(User)
    title=models.CharField("Title of Found Item",max_length=50)
    description=models.CharField("Short description of found item",max_length=300)
    created=models.DateTimeField("Post Created At",auto_now_add=True)
    location=models.CharField("location where item was found",max_length=100)
    contactEmail=models.EmailField("Email of finder",max_length=50)
    contactPhone=models.CharField("Phone number of finder",max_length=10)
    image=models.CharField("Image of founded item",max_length=300)
    ownerFound=models.BooleanField("Item owner found or not", default=False)
