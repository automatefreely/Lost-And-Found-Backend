from django.db import models
from ..user.models import User
# Create your models here.
class Feedback(models.Model):
    USER_EXPERIENCE=(
        ('1','Very Unsatisfied'),('2','Unsatisfied'),('3','Neutral'),('4','Satisfied'),('5','Very Satisfied')
    )
    user=models.ForeignKey(User)
    comment=models.CharField(max_length=500)
    user_experience=models.CharField(max_length=1,choices=USER_EXPERIENCE)
