import os
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_404_NOT_FOUND as ST_404
)


class registerAPI(APIView):
    permission_class=(AllowAny,)

    def return_errors(self,dic):
        err={}
        keys= dic.keys()
        for k in keys:
            if k =='password':
                x = dic[k][0].split(".")
                title= x[0] + '.' + x[1] + '.'
                err[k]= title
            else:
                err[k]= dic[k][0].capitalize()
        return err

    def post(self, request):
        data = request.data.copy()
        serializer= UserSerializer(data=data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"User created successfully","User":serializer.data}, status=ST_201)
            
        else:
            err= self.return_errors(serializer.errors)
            return Response({"Error":err},status=ST_400)
            
