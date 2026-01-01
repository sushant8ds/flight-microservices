from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, PlaceViewSet, WeekViewSet, PassengerViewSet
from . import gui_views

router = DefaultRouter()
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'places', PlaceViewSet, basename='place')
router.register(r'weeks', WeekViewSet, basename='week')
router.register(r'passengers', PassengerViewSet, basename='passenger')

urlpatterns = [
    path('', include(router.urls)),
    path('gui/flights/', gui_views.flight_list, name='gui_flight_list'),
    path('gui/places/', gui_views.place_list, name='gui_place_list'),
]
