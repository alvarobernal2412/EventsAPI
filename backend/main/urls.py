from django.urls import path
from main import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    #Calendar methods - Post, Put and Delete
    path('calendar/', views.CalendarView.as_view()),

    #Events methods - Get and Post 
    path('events/', views.EventView.as_view()),
    path('events/<int:pk>/' , views.EventIdView.as_view()),

    #Path to create the Daily JSON Web Token and the refresh code to create the Weekly token
    path('auth/token/', TokenObtainPairView.as_view()),
    #Path to create the Weekly token with the code from auth/token 
    path('auth/refreshToken/', TokenRefreshView.as_view()),
]