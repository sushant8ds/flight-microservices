from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Flight, Place

def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flights/gui_flight_list.html', {'flights': flights})

def place_list(request):
    places = Place.objects.all()
    return render(request, 'flights/gui_place_list.html', {'places': places})
