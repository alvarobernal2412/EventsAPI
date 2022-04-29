from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Event(models.Model):
    username = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    day = models.CharField(max_length=50)
    month = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    def __str__(self):
        return self.username
