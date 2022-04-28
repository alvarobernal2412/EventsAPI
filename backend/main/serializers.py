from datetime import date

from rest_framework import serializers
from .models import User
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=150,write_only=True)

    class Meta:
        model = User
        fields = ('username','password')
    
    def validate(self, args):
        username = args.get('username',None)
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'username':('Username already exists')})
        return super().validate(args)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
