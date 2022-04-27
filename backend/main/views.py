import os

from django.http import JsonResponse
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_404_NOT_FOUND as ST_404
)

class RegisterAPI(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data.copy()
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username).exists():
            err = "Ya existe un usuario registrado con el mismo nombre"
            return Response({"error":err},status=ST_400)       
        else:
            User.objects.create(username=username, password=password)
            return Response({"mensaje":"Usuario registrado correctamente"},status= ST_201)

class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = list(User.objects.values())
        if len(users) > 0:
            res = {"mensaje":"Petición realizada con éxito", "users": users}
        else:
            res = {"mensaje":"No existe ningún usuario"}
        return JsonResponse(res)
