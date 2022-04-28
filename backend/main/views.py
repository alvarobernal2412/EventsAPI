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
from .serializers import UserSerializer

class userAPI(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "User created successfully","User": serializer.data}, status=ST_201
                )
        return Response({"Errors":serializers.errors}, status= ST_400)
