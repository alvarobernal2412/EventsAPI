from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username

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
