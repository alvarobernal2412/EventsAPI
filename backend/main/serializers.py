from datetime import date

from django.contrib.auth.models import User as userModel
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User

