from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet
from . import gui_views

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('gui/bookings/', gui_views.booking_list, name='gui_booking_list'),
]
