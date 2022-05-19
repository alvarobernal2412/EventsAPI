from calendar import calendar
from importlib.resources import path
import os
import json
from re import S
from urllib import request

from django.shortcuts import redirect ,  render
from django.shortcuts import get_object_or_404

from main import urls

from . import models
from main.models import Calendar,Event
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics, filters
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
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import    (CreateCalendarSerializer, CalendarIdSerializer, UserSerializer,
                            SwaggerUserSerializer, CreateEventSerializer,
                             SwaggerEventSerializer ,EventSerializer)
from django.contrib.auth.models import User

from .services import get_weather


#Class to define Calendar methods 
class CalendarView(APIView):
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

    #Below appears the code to generate the body in Swagger documentation
    @swagger_auto_schema(request_body=UserSerializer)
    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        serializer= CreateCalendarSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Calendar successfully created", "user": serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"error": err},status=ST_400)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self,request):
        #If an user is not authenticated, throw the 401 error.
        if request.user.is_anonymous:
            return Response({"Error":"You must authenticate to update your user"},status=ST_401)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"User succesfully updated":serializer.data["username"]}, status=ST_200)

    def delete(self, request):
        #If an user is not authenticated, throw the 401 error.
        if request.user.is_anonymous:
            return Response({"Error":"You must authenticate to delete your calendar and user"},status=ST_401)

        #Now we delete the calendar and the user without using id , just using the JSON Web token
        calendar = Calendar.objects.get(user=request.user)
        calendar.delete()
        pk = request.user.id
        user=get_object_or_404(User,pk=pk)
        user.delete()
        return Response(status=ST_204)
 
           
#Class to define Events methods 
class EventView(APIView):
    permission_classes= (IsAuthenticated,)  

    filter_backends = (DjangoFilterBackend,)

    serializer_class = EventSerializer
    filterset_fields = ['eventName', 'date']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
    def get_queryset(self, request):
        query = Event.objects.all()
        return query

    #paramConfig = openapi.Parameter('eventName',in_=openapi.IN_QUERY,description='Event Name',type=openapi.TYPE_STRING)
    @swagger_auto_schema()
    def get(self, request):
        calendarId = Calendar.objects.get(user=request.user)
        events = self.filter_queryset(self.get_queryset(request)).filter(calendar=calendarId)
        serializer_class = CreateEventSerializer(events, many=True)

        if len(events) > 0:
            return Response(serializer_class.data)
        else:
            res = {"message": "There are no events created yet"}
            return Response(res, status=ST_404)
    
    def returnErrors(self,dic):
        err={}
        keys=dic.keys()
        for k in keys:
                err[k]= dic[k][0].capitalize()
        return err
 
    @swagger_auto_schema(request_body=EventSerializer)
    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        calendar = Calendar.objects.get(user=request.user)
        data['calendar'] = calendar.id
        if 'city' and 'time' in request.data:
            data['weather'] = get_weather(data['city'], data['date'], data['time'])
            if data['weather'] is None:
                data['weather'] = "Weather is only available within the next 5 days"
            message="Event successfully created"
        else:
            data['weather']='Undefined'
            message="Event successfully created. If you want to get the weather, time and city are required"
        
        
        serializer= CreateEventSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": message, "event": serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"Error":err},status=ST_400)  



class EventIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Event.objects.get(id=pk)
        except Event.DoesNotExist:
            raise Response(ST_404)

    @swagger_auto_schema(request_body=EventSerializer)
    def put(self, request , pk):
        event = self.get_object(pk)
        calendarId = Calendar.objects.get(user=request.user)
        if event.calendar != calendarId:
            return Response("You can't edit another user's event", status=ST_401)
        else:
            data = request.data.copy()
            data["calendar"]=calendarId.id
            if "eventName" not in data:
                data["eventName"]= event.eventName
            if "date" not in data:
                data["date"]= event.date
            serializer= CreateEventSerializer(event,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=ST_200)
            return Response(serializer.errors , status=ST_400)


    @swagger_auto_schema()
    @csrf_exempt    
    def delete(self, request , pk):
        event = self.get_object(pk)
        calendarId = Calendar.objects.get(user=request.user)
        eventList =  []
        eventList.append(event)
        if len(eventList) == 0:
            res= {"message" : "This event does not exist"} # No funciona correctamente
            return Response(res , status=ST_404)
        elif event in Event.objects.filter(calendar=calendarId): 
            event.delete()
            res= {"message" : "Event successfully deleted"}
            return Response(res , status=ST_204)
        else:
            res= {"message" : "You can only delete events form your calendar"}
            return Response(res , status=ST_401)

           
    