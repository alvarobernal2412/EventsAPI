from django.urls import path
from main import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('calendar/', views.CalendarView.as_view()),
    path('calendar/<int:pk>/', views.CalendarView.as_view()),
    path('events/', views.EventView.as_view()),
    path('events/', views.FilterEventView.as_view()),
    path('events/<event_id>/' , views.EventView.delete_event),
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/refreshToken/', TokenRefreshView.as_view()),
]