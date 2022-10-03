from django.db import models
# Create your models here.
USER_EXPERIENCE=(
    ('1','Very Unsatisfied'),('2','Unsatisfied'),('3','Neutral'),('4','Satisfied'),('5','Very Satisfied')
)
class Feedback(models.Model):
    user_id = models.CharField("User uid", max_length=20)
    user_name = models.CharField("User name", max_length=100)
    comment=models.CharField(max_length=500)
    user_experience=models.CharField(max_length=1,choices=USER_EXPERIENCE)
    created=models.DateTimeField("Post Created At",auto_now_add=True)
