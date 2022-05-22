from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_401_UNAUTHORIZED as ST_401,
    HTTP_404_NOT_FOUND as ST_404,
)
from rest_framework.test import APIClient
from main.models import Calendar, Event, GlobalEvent,User
from datetime import date

# No solo se deben añadir test positivos, tambien se deben probar errores

class AuthenticationTestCase(TestCase):
    access = ""
    refresh = ""
    def setUp(self):
        self.user = User(
            username='testingUser',
        )
        self.user.set_password('admin1234')
        self.user.save()

        self.calendar= Calendar(
            user=self.user
        )
        self.calendar.save()
        client= APIClient()
        
        tokenResponse = client.post(
            '/api/auth/token/',{
                'username':'testingUser',
                'password':'admin1234'
            },format='json')
        response = client.post(
            '/api/auth/refreshToken/',{
                'refresh': tokenResponse.data['refresh'] #Here can be a coma at the end
            }, format='json')
        
        self.access=response.data['access']

    def testCalendar(self):
        client = APIClient()
        response = client.post('/api/calendar/',{
            'username':'testingUser2',
            'password':'admin12345'
        }, format='json')

        self.assertEqual(response.status_code, ST_201)#Calendar successfully created
    
    def testRefreshToken(self):
        client= APIClient()
        
        tokenResponse = client.post(
            '/api/auth/token/',{
                'username':'testingUser',
                'password':'admin1234'
            },format='json')
        response = client.post(
            '/api/auth/refreshToken/',{
                'refresh': tokenResponse.data['refresh'] #Here can be a coma at the end
            }, format='json')
        self.access=response.data['access']

        self.assertEqual(response.status_code,ST_200)#Token successfully created

    
    def testModifyCalendar(self):
        client= APIClient()
        response = client.put('/api/calendar/',{
            'password':'contra1234'
        },HTTP_AUTHORIZATION=('JWT '+self.access))
        
        self.assertEqual(response.status_code, ST_204)#Password successsfully changed
    
    def testDeleteCalendar(self):
        client=APIClient()
        response = client.delete('/api/calendar/',HTTP_AUTHORIZATION=('JWT '+self.access))
        self.assertEqual(response.status_code, ST_204)#Calendar successfully deleted
    
class EventTestCase(TestCase):

    def setUp(self):

        #Base constructor for testing

        self.user = User(
            username='exampleUser',
        )
        self.user.set_password('contra1234')
        self.user.save()

        self.calendar= Calendar(
            user=self.user
        )
        self.calendar.save()
        client= APIClient()
        tokenResponse = client.post(
            '/api/auth/token/',{
                'username':'exampleUser',
                'password':'contra1234'
            },format='json')
        refreshResponse = client.post(
            '/api/auth/refreshToken/',{
                'refresh': tokenResponse.data['refresh'] #Here can be a coma at the end
            }, format='json')
        
        self.event= Event(
            eventName= "Event Test 1",
            description="Event test description 1",
            city="Seville",
            date="2022-05-21",
            time="13:56:00",
            calendar=self.calendar
        )
        self.event2= Event(
            eventName= "Event Test 2",
            description="Event test description 2",
            city="Seville",
            date="2022-05-21",
            time="13:56:00",
            calendar=self.calendar
        )
        self.event.save()
        self.event2.save()
        self.access= refreshResponse.data['access']

        
    def testEvent(self):
        client= APIClient()
        response= client.post('/api/events/',{
            "eventName": "Event Test 3",
            "description": "Event test description 3",
            "city": "Seville",
            "date": "2022-05-21",
            "time": "12:30:00"},
            HTTP_AUTHORIZATION=('JWT '+self.access))

        self.assertEqual(response.status_code, ST_201)#Events successfully created

    def testSearchEvents(self):
        client= APIClient()
        response = client.get('/api/events/',
                              HTTP_AUTHORIZATION=('JWT '+self.access))

        self.assertEqual(response.status_code, ST_200)#Events get successfully done

        response2 = client.get('/api/events/', format='json')
        
        self.assertEqual(response2.status_code,ST_401)#If some user try to get events without JWT token.

        results = response.json()
        i = 0
        for _ in results:
            i=i+1
        self.assertEqual(i, 2)#Compare if the event recently created exists

    def testModifyEvents(self):
        client=APIClient()
        response = client.put('api/events/'+str(self.event.id)+'/',{
            "description":"Event test changed description"
        }
        ,HTTP_AUTHORIZATION=('JWT '+self.access))
        self.eventUpdated = Event.objects.get(pk=self.event.id)
        self.assertEqual(response.status_code,ST_204)#Event successfully changed
        self.assertEqual(self.eventUpdated.description, "Event test changed description")#Compare if the description has been updated
    
    def testDeleteEvents(self):
        client=APIClient()
        response= client.delete('/api/events/'+str(self.event2.id)+'/',HTTP_AUTHORIZATION=('JWT '+self.access))
        self.assertEqual(response.status_code, ST_204)#Event successfully deleted