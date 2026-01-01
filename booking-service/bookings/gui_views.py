from django.shortcuts import render
from .models import Ticket

def booking_list(request):
    bookings = Ticket.objects.all()
    return render(request, 'bookings/gui_booking_list.html', {'bookings': bookings})
