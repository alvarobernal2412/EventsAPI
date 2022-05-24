from calendar import calendar
from importlib.resources import path
import os
import json
from re import S
from urllib import request
from datetime import datetime,date 

from django.shortcuts import redirect ,  render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from main import urls

from . import models
from main.models import Calendar,Event,GlobalEvent
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
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import    (CreateCalendarSerializer, CalendarIdSerializer, UserSerializer,
                            SwaggerUserSerializer, CreateEventSerializer,
                            SwaggerEventSerializer ,EventSerializer, PutEventSerializer,
                            GlobalEventSerializer, GetGlobalEventSerializer)
from django.contrib.auth.models import User
from .services import (get_weather, get_global_events, post_global_event,delete_global_events, get_global_events_id)
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
    @swagger_auto_schema(request_body=UserSerializer,responses={201: "Calendar successfully created",400: "Bad request (This status code gives more information of the request error)"})
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

    @swagger_auto_schema(request_body=UserSerializer,responses={204: "No Content (Calendar successfully updated)",401: "Unauthorized (You need the JWT token to change your calendar information)"})
    def put(self,request):
        #If an user is not authenticated, throw the 401 error.
        if request.user.is_anonymous:
            return Response({"Error":"You must authenticate to update your user"},status=ST_401)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"User succesfully updated":serializer.data["username"]}, status=ST_204)

    @swagger_auto_schema(responses={204: "No Content (Successfully deleted)",401: "Unauthorized (You need the JWT token to delete your calendar information)"})
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
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
    
    queryset =Event.objects.all()
    serializer_class = EventSerializer
    

    search_fields = ('eventName','weather',)
    filterset_fields = ('eventName','weather','completed')
    ordering_fields = ('eventName','date')
    

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def stringToDate(dateStr):
        return (datetime.strptime(dateStr, '%m-%d-%Y').date())

    paramConfig = openapi.Parameter('eventName',in_=openapi.IN_QUERY,description='Event name filter',type=openapi.TYPE_STRING)
    paramConfig2 = openapi.Parameter('weather',in_=openapi.IN_QUERY,description='Weather filter',type=openapi.TYPE_STRING)
    paramConfig3 = openapi.Parameter('ordering',in_=openapi.IN_QUERY,description='You can order by eventName and date (Include "-" for reversed order)',type=openapi.TYPE_STRING)
    paramConfig4 = openapi.Parameter('search',in_=openapi.IN_QUERY,description='You can search for eventName or weather (If it contains the word)',type=openapi.TYPE_STRING)
    paramConfig5 = openapi.Parameter('limit',in_=openapi.IN_QUERY,description='Responses number',type=openapi.TYPE_NUMBER)
    paramConfig6 = openapi.Parameter('offset',in_=openapi.IN_QUERY,description='Index number',type=openapi.TYPE_NUMBER)
    paramConfig7 = openapi.Parameter('completed',in_=openapi.IN_QUERY,description='Completed events filter',type=openapi.TYPE_BOOLEAN)
    getResponse= openapi.Response('Event structure below', CreateEventSerializer(many=True))
    
    @swagger_auto_schema(manual_parameters=[paramConfig,paramConfig2,paramConfig5,paramConfig6,paramConfig3,paramConfig4,paramConfig7], responses={200: getResponse,404: "No events found"}) #paramConfig5,paramConfig6
    def get(self, request):
        limit= request.GET.get('limit') 
        offset= request.GET.get('offset') 
        calendarId = Calendar.objects.get(user=request.user)
        if (limit is None) and (offset is not None):
            events = self.filter_queryset(self.queryset).filter(calendar=calendarId)[int(offset):]
        elif (offset is None) and (limit is not None):
            events = self.filter_queryset(self.queryset).filter(calendar=calendarId)[:int(limit)]
        elif (limit is None) and (offset is None):
            events = self.filter_queryset(self.queryset).filter(calendar=calendarId)
        else:
            events = self.filter_queryset(self.queryset).filter(calendar=calendarId)[int(offset):(int(offset)+int(limit))]
        
        
        serializer_class = CreateEventSerializer(events, many=True)
        if len(events) > 0:
            return Response(serializer_class.data,status=ST_200)
        else:
            res = {"message": "No events found"}
            return Response(res, status=ST_404)
    
    def returnErrors(self,dic):
        err={}
        keys=dic.keys()
        for k in keys:
                err[k]= dic[k][0].capitalize()
        return err
 
    @swagger_auto_schema(request_body=EventSerializer,responses={201: "Event successfully created",400: "Bad request (This status code gives more information of the request error)"})
    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        calendar = Calendar.objects.get(user=request.user)
        data['calendar'] = calendar.id

        date = data['date']
        date = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.combine(datetime.today(), datetime.min.time())
        days_diff = (date-today).days

        if ('city' in request.data) and ('time' in request.data):
            if  0 <= days_diff <= 4:
                data['weather'] = get_weather(data['city'], data['date'], data['time'])
            else:
                data['weather'] = "Weather is only available within the next 5 days"
            message="Event successfully created"
        else:
            data['weather']='Undefined'
            message="Event successfully created. If you want to get the weather, time and city are required"
        data['completed']=False
        
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
            return Response(ST_404)

    @swagger_auto_schema(request_body=PutEventSerializer,responses={204: "No Content (Event successfully updated)",400: "Bad request (This status code gives more information of the request error)"})
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
            if "time" not in data:
                data["time"]= event.time
            if "city" not in data:
                data["city"]= event.city
            if "completed" not in data:
                data["completed"]= event.completed

            date = str(data['date'])
            date = datetime.strptime(date, "%Y-%m-%d")
            today = datetime.combine(datetime.today(), datetime.min.time())
            days_diff = (date-today).days

            if (data["city"]=='' and data["time"] is None):
                data['weather']='Undefined'
                #message="Event successfully updated. If you want to get the weather, time and city are required"
            elif data["city"]=='':
                data['weather']='Undefined'
                #message="Event successfully updated. If you want to get the weather, city is required"
            elif data["time"] is None:
                data['weather']='Undefined'
                #message="Event successfully updated. If you want to get the weather, time is required"
            else:
                if  0 <= days_diff <= 4:
                    data['weather'] = get_weather(data['city'], str(data['date']), str(data['time']))
                else:
                    data['weather'] = "Weather is only available within the next 5 days"
                #message="Event successfully updated" 

            
            serializer= CreateEventSerializer(event,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=ST_204)#{"message": message, "event": serializer.data} 204 dont have response body
            return Response(serializer.errors, status=ST_400)


    @swagger_auto_schema(responses={204: "No Content (Event successfully deleted",404: "Event not found in your calendar or deleted yet"})
    @csrf_exempt    
    def delete(self, request , pk):
        event = self.get_object(pk)
        calendarId = Calendar.objects.get(user=request.user)
        eventList =  []
        eventList.append(event)
        if event in Event.objects.filter(calendar=calendarId): 
            event.delete()
            res= {"message" : "Event successfully deleted"}
            return Response(res , status=ST_204)
        else:
            res= {"message" : "You can only delete events that exist on your calendar"}
            return Response(res , status=ST_404)

           

class GlobalEventsView(APIView):

    def returnErrors(self,dic):
        err={}
        keys=dic.keys()
        for k in keys:
                err[k]= dic[k][0].capitalize()
        return err
    
    @swagger_auto_schema(responses={200: "Search results with matching criteria",400: "Bad Request"})
    def get(self,request):
        globalEvents= get_global_events()
        serializer_class = GetGlobalEventSerializer(globalEvents, many=True)

        if len(globalEvents) > 0:
            return Response(serializer_class.data)
        else:
            res = {"Message": "There are no events created yet"}
            return Response(res, status=ST_404)

    @swagger_auto_schema(request_body=GlobalEventSerializer,responses={201: "Global event correctly created",400: "Bad Request"})
    def post(self,request):
        data = request.data.copy()
        name=data["name"]
        description=data["description"]
        organizer=data["organizer"]
        category=data["category"]
        location=data["location"]
        date=data["date"]
        (eventCode,eventResponse) = post_global_event(name,description,organizer,category,location,date)
        id=eventResponse["id"]
        data["id"] = id
        serializer= GetGlobalEventSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({eventCode:"Global Event successfully created", "Event": eventResponse},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"Error":err},status=ST_400)  
    
class GlobalEventsIdView(APIView):
    @swagger_auto_schema(responses={204: "No Content (Global event deleted)",401:"You can only delete global events created from EventsAPI",404: "Global event not found"})
    def delete(self, request, pk):
        try:
            globalEventInDB = GlobalEvent.objects.get(id=pk)
            code = delete_global_events(pk)
            if code == 204:
                globalEventInDB.delete()
                res= {"message" : "Global event successfully deleted"}
                return Response(res, status=ST_204)
            else:
                res= {"message" : "Global event not found"}
                return Response(res, status=ST_404)
        except GlobalEvent.DoesNotExist:
            res= {"message" : "You can only delete global events created from EventsAPI"}
            return Response(res, status=ST_401)
