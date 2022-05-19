from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    id=models.AutoField(primary_key=True) 
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
        
class Event(models.Model):
    id=models.AutoField(primary_key=True) 
    eventName=models.CharField(max_length=50)
    description=models.CharField(max_length=500, blank=True)
    city=models.CharField(max_length=50, blank=True) 
    date=models.DateField()
    time=models.TimeField(blank=True)
    weather=models.CharField(max_length=500, blank=True, null=True)
    calendar=models.ForeignKey(Calendar,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
        
