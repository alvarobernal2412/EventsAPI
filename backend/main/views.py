import os

from . import models
from main.models import Calendar
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_404_NOT_FOUND as ST_404,
)
from .serializers import CreateCalendarSerializer

class CalendarView(generics.CreateAPIView):
    
    def returnErrors(self,dic):
        err={}
        keys=dic.keys()
        for k in keys:
            if k == 'password':
                x= dic[k][0].split(".")
                title=x[0]+'.'+x[1]+'.'
                err[k]= title
            else:
                err[k]= dic[k][0].capitalize()
        return err


    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        serializer= CreateCalendarSerializer(data=data,context ={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Calendar successfully created", "user":serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"Error":err},status=ST_400)

#class eventView(generics.CreateAPIView):

#    def get(self, request):
#        events = list(Event.objects.values())
#        if len(events) > 0:
#            res = {'events': events}
#            return Response(res, status=ST_200)
#        else:
#            res = {'message': 'Events not found'}
#            return Response(res, status=ST_404)
