from django.urls import path
from main import views

urlpatterns = [
    path('calendar/', views.CalendarView.as_view()),
    #path('event/', views.eventView.as_view()),
]