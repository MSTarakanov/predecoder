from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class IntelDescription(models.Model):
    counter = models.IntegerField(default=0)
    example_id = models.IntegerField(default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
