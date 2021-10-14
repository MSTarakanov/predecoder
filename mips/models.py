from django.db import models
from django.contrib.auth.models import User


class MipsDescription(models.Model):
    counter = models.IntegerField(default=0)
    stream = models.CharField(default="", max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mips_user')
