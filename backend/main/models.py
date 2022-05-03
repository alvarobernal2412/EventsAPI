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
    description=models.CharField(max_length=500)
    date= models.DateField()
    time= models.TimeField()
    weather=models.CharField(max_length=500)
    calendar=models.ForeignKey(Calendar,on_delete=models.CASCADE)

    def __str__(self):
        return self.id
        


#La fecha dentro de evento es susceptible a ser cambiada dependiendo de si da o no problemas por la doble dependencia de estos
