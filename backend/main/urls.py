from django.urls import path
from main import views

urlpatterns = [
    path('calendar/', views.CalendarView.as_view()),
    path('calendar/<int:pk>/', views.CalendarView.as_view()),
]