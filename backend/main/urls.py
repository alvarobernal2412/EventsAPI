from django.urls import path
from main import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('calendar/', views.CalendarView.as_view()),
    path('calendar/id/', views.CalendarIdView.as_view()),
    path('events/', views.EventView.as_view()),
    path('events/<int:pk>/' , views.EventIdView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/refreshToken/', TokenRefreshView.as_view()),
]