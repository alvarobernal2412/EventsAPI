from django.urls import path
from main import views

urlpatterns = [
    path('users/', views.userView.as_view()),
    path('events/', views.eventView.as_view()),
]