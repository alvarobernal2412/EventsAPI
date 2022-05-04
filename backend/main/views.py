import os
import json

from . import models
from main.models import Calendar,Event
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_401_UNAUTHORIZED as ST_401,
    HTTP_404_NOT_FOUND as ST_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated


from .serializers import CreateCalendarSerializer, UserSerializer, CreateEventSerializer

class CalendarView(generics.CreateAPIView):
    permission_classes= (AllowAny,)
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
        serializer= CreateCalendarSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Calendar successfully created", "user":serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"Error":err},status=ST_400)

    def put(self,request, pk):
        pass
        #if request.user != Calendar.objects.filter(pk=pk).user:
        #    return Response("You cannot change another user data", status=ST_401)
        #jd = json.loads(request.body)
        #calendar = list(Calendar.objects.filter(pk=pk).values())
        #if len(calendar) > 0 : 
        #    calendar= calendar.objects.get(pk=pk) 
        #    calendar.user.username = jd['username']
        #    calendar.user.password = jd['password']
        #    calendar.save()
        #    return Response({"Message":"Calendar successfully updated", "user":request.data}, status=ST_204)
        #return Response(status=ST_404)
            

class EventView(generics.CreateAPIView):

    permission_classes= (IsAuthenticated,)

    def returnErrors(self,dic):
        err={}
        keys=dic.keys()
        for k in keys:
                err[k]= dic[k][0].capitalize()
        return err

    def get(self, request):
        #event = Events.objects.filter(user=request.user)
        events = list(Event.objects.values())
        if len(events) > 0:
            res = {'events': events}
            return Response(res, status=ST_200)
        else:
            res = {'message': 'Events not found'}
            return Response(res, status=ST_404)

    
    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        serializer= CreateEventSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Event successfully created", "event":serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"Error":err},status=ST_400)     
    