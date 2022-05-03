from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Calendar, Day ,Event


class CreateCalendarSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields= ('username','password')
    
    def create(self,validatedData):
        user = User.objects.create(username=validatedData['username'])
        user.set_password(validatedData['password'])
        user.save()
        Calendar.objects.create(user=user)
        return user
