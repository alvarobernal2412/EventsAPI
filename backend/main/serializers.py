from dataclasses import field, fields
from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Calendar ,Event


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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

    def change(self,validatedData):
        user = User.objects.change(username=validatedData['username'])
        user.set_password(validatedData['password'])
        user.save()
        return user

class SwaggerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'date', 'time', 'weather', 'calendar')

    def create(self, validatedData):
        event = Event.objects.create(
            eventName=validatedData['eventName'], 
            description=validatedData['description'],
            date=validatedData['date'], 
            time=validatedData['time'],
            weather=validatedData['weather'], 
            calendar=validatedData['calendar'],  
        )
        event.save()
        return event
        #calendar tiene que ser modificado de manera que se auto asocie gracias a request.user

class SwaggerEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'date', 'time', 'weather', 'calendar')

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'date', 'time', 'weather', 'calendar')
