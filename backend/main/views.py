import os
import json

from . import models
from main.models import Calendar, Event
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
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import    (CreateCalendarSerializer, UserSerializer,
                            SwaggerUserSerializer, CreateEventSerializer,
                            EventSerializer, SwaggerEventSerializer, )

class CalendarView(generics.CreateAPIView):
    permission_classes= (AllowAny,)
    swagger_tags=["Endpoints de registro"]  

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

    @swagger_auto_schema(request_body=UserSerializer)
    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        serializer= CreateCalendarSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Calendar successfully created", "user":serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"error":err},status=ST_400)

    def put(self, request, pk):
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
            

class EventView(generics.GenericAPIView):
    permission_classes= (IsAuthenticated,)
    swagger_tags=["Endpoints de eventos"]   
    
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
            res = {"events": events}
            return Response(res, status=ST_200)
        else:
            res = {"message": "Events not found"}
            return Response(res, status=ST_404)

    @swagger_auto_schema(request_body=SwaggerEventSerializer)
    @csrf_exempt
    def post(self, request):
        data = request.data.copy()
        serializer= CreateEventSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Event successfully created", "event":serializer.data},status=ST_201)
        else:
            err= self.returnErrors(serializer.errors)
            return Response({"error":err},status=ST_400)  

class EventsIdView(APIView):
    permission_classes= (IsAuthenticated,)
    
    def get_object(self, pk):
        event = list(Event.objects.filter(id=pk))
        if len(event) > 0:
            return event
        res = {"message": "That event does not exist"}
        return Response(res, status=ST_404)
    
    def delete(self, request, pk):
        event = list(self.get_object(pk))
        if len(event) > 0:
            Event.objects.filter(pk=id).delete()
            res = {"message":"Event successfully deleted"}
            return Response(res, status=ST_204)
        else:
            res = {"message": "That event does not exist"}
            return Response(res, status=ST_404)

    def get(self, request, pk):
        # self.delete(request, pk)
        return Response(EventSerializer(get_object_or_404(Event, pk=pk)).data)
    
    
"""
    def delete(self, request, pk):
        try:
            event = self.get_object(pk)
            if event.calendar.user.id == request.user.id:
                event.delete()
                res = {"message":"Event successfully deleted"}
                return Response(res, status=ST_204)
            else:
                return Response("You can not delete an event that does not own you", status=ST_401)
        except Exception as e:
            res = {"message": "That event does not exist"}
            return Response(res, status=ST_404)
"""
"""
    def get(self, request, pk):
        pk = request.events.id
        return Response(EventSerializer(get_object_or_404(Event, pk=id)).data)
    """
"""
    def delete(self, request):
        pk = request.event.id
        event=get_object_or_404(Event,pk=id)
        event.delete()
        return Response(status=ST_204)
"""
    

           
class FilterEventView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description']
    