from django.shortcuts import render
from flights.models import Flight, Place

def index(request):
    return render(request, 'index.html')

def search(request):
    flights = []
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    if origin and destination:
        flights = Flight.objects.filter(origin__code__icontains=origin, destination__code__icontains=destination)
    return render(request, 'search.html', {'flights': flights, 'origin': origin, 'destination': destination})
