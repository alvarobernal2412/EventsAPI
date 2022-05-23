from dataclasses import field, fields
from datetime import date
from datetime import time

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Calendar, Event, GlobalEvent

#Calendar serializers
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

#User serializers
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

#Events serializers
class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'city', 'date', 'time', 'weather','done', 'calendar')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('eventName', 'description', 'city', 'date', 'time')


class PutEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('eventName', 'description', 'city', 'date', 'time','done')


#Serializer that gives Swagger Events structure
class SwaggerEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'eventName', 'description', 'city', 'date', 'time', 'weather', 'calendar')

#Global Events serializer
class GlobalEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalEvent
        fields = ('name', 'description', 'organizer', 'category', 'location','date')

class GetGlobalEventSerializer(serializers.ModelSerializer):

    class Meta: 
        model = GlobalEvent
        fields = '__all__'

        