from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    id=models.AutoField(primary_key=True) 
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
        
class Event(models.Model):
    id=models.AutoField(primary_key=True) 
    eventName=models.CharField(max_length=50)
    description=models.CharField(max_length=500, blank=True)
    city=models.CharField(max_length=50, blank=True, default='') 
    date=models.DateField()
    time=models.TimeField(blank=True, null=True)
    weather=models.CharField(max_length=500, blank=True, default='') # Changed null=True by default because of being a Char
    completed=models.BooleanField(blank=True, default=False)
    calendar=models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class GlobalEvent(models.Model):
    id=models.CharField(max_length=50, primary_key=True)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    organizer=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    date=models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)
        
