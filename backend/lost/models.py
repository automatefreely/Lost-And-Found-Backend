from django.db import models
from secrets import token_urlsafe

class Lost(models.Model):
    id = models.CharField("Unique ID of lost item", max_length=10, primary_key=True, default=token_urlsafe(10))
    user_id = models.CharField("User uid", max_length=20)
    user_name = models.CharField("User name", max_length=100)
    title=models.CharField("Title of Lost Item", max_length=50)
    description=models.CharField("Short Description of Lost Item",max_length=300)
    created=models.DateTimeField("Post Created At",auto_now_add=True)
    location=models.CharField("location where item was lost",max_length=100)
    lostDate=models.DateTimeField("Date when item was lost")
    contactEmail=models.EmailField("Email of owner",max_length=50)
    contactPhone=models.CharField("Phone number of owner",max_length=10)
    image=models.CharField("Image of lost item",max_length=300)
    found=models.BooleanField("Item found or not", default=False)