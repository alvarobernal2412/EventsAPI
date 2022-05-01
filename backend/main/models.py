from django.db import models

class User(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    password=models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Calendar(models.Model):
    id=models.AutoField(primary_key=True) 
    calendar=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)

class Day(models.Model):
    date= models.DateTimeField(primary_key=True)
    weather=models.CharField(max_length=500)
    calendar=models.ForeignKey(Calendar,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.date)

class Event(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    day=models.ForeignKey(Day,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

#La fecha dentro de evento es susceptible a ser cambiada dependiendo de si da o no problemas por la doble dependencia de estos
