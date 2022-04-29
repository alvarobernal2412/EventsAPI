from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    eventName=models.CharField(max_length=500)
    description=models.CharField(max_length=500)
    def __str__(self):
        return self.eventName

class Day(models.Model):
    date= models.DateTimeField(primary_key=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    weather=models.CharField(max_length=500)
    def __str__(self):
        return str(self.date)

class Calendar(models.Model):
    id = models.AutoField(primary_key=True) 
    calendarList=models.ForeignKey(Day,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.id


class CustomUser(models.Model):
    username=models.CharField(max_length=500,primary_key=True)
    calendar=models.OneToOneField(Calendar,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username



#La fecha dentro de evento es susceptible a ser cambiada dependiendo de si da o no problemas por la doble dependencia de estos
