import os
from . import models
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_404_NOT_FOUND,
)

class createUser(generics.CreateAPIView):
    @csrf_exempt
    def post(self, request):
        body = request.data
        name = body['username']
        models.CustomUser.objects.create(username=username)
        return Response(status=ST_201)

    #@csrf_exempt
    #def get(self, request):
    #    return Response(models.Users.objects.get())