from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.password_validation import validate_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])

    class Meta:
        model = User
        fields = ('username','password')

    def validate(self, value):
        username = value.get('username',None)
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user)
        return user
