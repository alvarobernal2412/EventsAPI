from dataclasses import field, fields
from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Calendar, Event

#Serializer that validates user password and set Calendar structure
class CreateCalendarSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields= ('username', 'password')
    
    def create(self, validatedData):
        user = User.objects.create(username=validatedData['username'])
        user.set_password(validatedData['password'])
        user.save()
        Calendar.objects.create(user=user)
        return user

class CalendarIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ['id',]

#Serializer that validates user password and set User structure
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

    def change(self,validatedData):
        user = User.objects.change(username=validatedData['username'])
        user.set_password(validatedData['password'])
        user.save()
        return user

#Serializer that gives Swagger user structure
class SwaggerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

#Serializer that sets Event structure
class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'date', 'time', 'weather','calendar')

    def create(self, validatedData):
        event = Event.objects.create(
            eventName=validatedData['eventName'], 
            description=validatedData['description'],
            date=validatedData['date'], 
            time=validatedData['time'],
            weather=validatedData['weather'],  
            calendar=validatedData['calendar']
        )
        event.save()
        return event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('eventName', 'description', 'date', 'time', 'weather')

#Serializer that gives Swagger Events structure
class SwaggerEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'date', 'time', 'weather', 'calendar')

