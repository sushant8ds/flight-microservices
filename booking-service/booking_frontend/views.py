from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from bookings.models import Ticket
from datetime import datetime

def bookings(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))
def bookings(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from bookings.models import Ticket
from datetime import datetime

def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            try:
                ticket = Ticket.objects.get(ref_no=ref)
                if ticket.user == request.user:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': 'User unauthorised'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return HttpResponse('User unauthorised')
    else:
        return HttpResponse('Method must be POST.')

def resume_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            ticket = Ticket.objects.get(ref_no=ref)
            if ticket.user == request.user:
                return render(request, 'flight/payment.html', {
                    'fare': ticket.total_fare,
                    'ticket': ticket.id
                })
            else:
                return HttpResponse('User unauthorised')
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Method must be post.')
def ticket_data(request, ref):
    # Minimal stub for ticket data API
    return JsonResponse({'error': 'Not implemented'}, status=501)

def get_ticket(request):
    # Minimal stub for get_ticket
    return HttpResponse('Not implemented', content_type='text/plain')

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from bookings.models import Ticket
import logging
import os
from django.conf import settings
from datetime import datetime, date, timedelta
import requests

def review(request):
    return render(request, 'flight/book.html')

def book(request):
    return render(request, 'flight/book.html')

def payment(request):
    return render(request, 'flight/payment.html')

def static_test_view(request):
    return render(request, 'flight/static_test.html')

def static_diagnostic_view(request):
    file_list = []
    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), settings.STATIC_ROOT))
    return HttpResponse('<br>'.join(file_list))

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, "flight/login.html")

def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "flight/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(request, "flight/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "flight/register.html")

def query_places(request, q):
    # TODO: Implement place autocomplete using your data model
    return JsonResponse([], safe=False)

def flight(request):
    return render(request, 'flight/search.html')

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from bookings.models import Ticket
import logging
import os
from django.conf import settings
from datetime import datetime, date, timedelta
import requests

def static_test_view(request):
    return render(request, 'flight/static_test.html')

def static_diagnostic_view(request):
    file_list = []
    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), settings.STATIC_ROOT))
    return HttpResponse('<br>'.join(file_list))

def index(request):
    logging.warning("[DEBUG] index view called, method=%s, GET=%s, POST=%s", request.method, dict(request.GET), dict(request.POST))
    today = date.today()
    context = {
        'min_date': today.strftime('%Y-%m-%d'),
        'max_date': (today + timedelta(days=365)).strftime('%Y-%m-%d'),
        'depart_date': today.strftime('%Y-%m-%d'),
        'return_date': '',
        'trip_type': '1',
        'seat': 'economy',
        'user': request.user,
    }
    return render(request, 'flight/index.html', context)

def bookings_list(request):
    bookings = Ticket.objects.all()
    return render(request, 'bookings.html', {'bookings': bookings})

def search_flights(request):
    logging.warning("[DEBUG] search_flights view called")
    flights = []
    error = None
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')
    date_val = request.GET.get('date', '')
    if request.method == 'POST':
        flight_id = request.POST.get('flight_id')
        if flight_id:
            return redirect(f'/book-flight/?flight_id={flight_id}')
    elif request.method == 'GET' and request.GET.get('search'):
        api_url = 'http://flight-service:8002/api/flights/'
        params = {}
        if origin:
            params['origin'] = origin
        if destination:
            params['destination'] = destination
        if date_val:
            params['date'] = date_val
        try:
            logging.warning(f"[DEBUG] Calling flight-service API: {api_url} params={params}")
            import time
            start = time.time()
            resp = requests.get(api_url, params=params, timeout=30)
            elapsed = time.time() - start
            logging.warning(f"[DEBUG] Response status: {resp.status_code}, elapsed={elapsed:.2f}s")
            if resp.status_code == 200:
                flights = resp.json()
            else:
                error = f"API error: {resp.text}"
        except Exception as e:
            logging.warning(f"[DEBUG] Exception: {e}")
            error = str(e)
    context = {
        'flights': flights,
        'error': error,
        'origin': origin,
        'destination': destination,
        'depart_date': date_val,
        'return_date': '',
        'trip_type': request.GET.get('TripType', '1'),
        'seat': request.GET.get('SeatClass', 'economy'),
        'debug_banner': True,
    }
    return render(request, 'flight/search.html', context)

@csrf_exempt
def book_flight(request):
    error = None
    success = None
    flight = None
    if request.method == 'GET':
        flight_id = request.GET.get('flight_id')
        if not flight_id:
            return HttpResponse('No flight selected.', status=400)
        api_url = f'http://flight-service:8002/api/flights/{flight_id}/'
        try:
            resp = requests.get(api_url, timeout=30)
            if resp.status_code == 200:
                flight = resp.json()
            else:
                error = f"API error: {resp.text}"
        except Exception as e:
            error = str(e)
        return render(request, 'flight/book.html', {'flight': flight, 'error': error})
    return HttpResponse('Invalid request method.', status=405)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, "flight/login.html")

def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "flight/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(request, "flight/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "flight/register.html")

def contact(request):
    return render(request, 'flight/contact.html')

def privacy_policy(request):
    return render(request, 'flight/privacy-policy.html')

def terms_and_conditions(request):
    return render(request, 'flight/terms.html')

def about_us(request):
    return render(request, 'flight/about.html')
    error = None
    success = None
    flight = None
    if request.method == 'GET':
        flight_id = request.GET.get('flight_id')
        if not flight_id:
            return HttpResponse('No flight selected.', status=400)
        # Fetch flight details from flight-service API
        api_url = f'http://flight-service:8002/api/flights/{flight_id}/'
        try:
            logging.warning(f"[DEBUG] Calling flight-service API: {api_url}")
            resp = requests.get(api_url)
            logging.warning(f"[DEBUG] Response status: {resp.status_code}")
            if resp.status_code == 200:
                flight = resp.json()
            else:
                error = f"Flight not found: {resp.text}"
        except Exception as e:
            logging.warning(f"[DEBUG] Exception: {e}")
            error = str(e)
        return render(request, 'book_flight.html', {'flight': flight, 'error': error})
    elif request.method == 'POST':
        # Collect booking data from form
        flight_id = request.POST.get('flight_id')
        passenger_names = request.POST.get('passenger_names', '').split(',')
        seat_class = request.POST.get('seat_class')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        # Fetch flight details for booking fields
        api_url = f'http://flight-service:8002/api/flights/{flight_id}/'
        try:
            resp = requests.get(api_url)
            if resp.status_code == 200:
                flight = resp.json()
            else:
                error = f"Flight not found: {resp.text}"
        except Exception as e:
            error = str(e)
        if not flight:
            return render(request, 'book_flight.html', {'flight': None, 'error': error})
        # Prepare booking data
        booking_data = {
            'ref_no': f'REF{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'flight_id': flight_id,
            'passenger_names': passenger_names,
            'flight_ddate': flight['depart_time'],
            'flight_adate': flight['arrival_time'],
            'flight_fare': flight.get('fare', 1000),
            'other_charges': 0,
            'coupon_used': '',
            'coupon_discount': 0,
            'total_fare': flight.get('fare', 1000),
            'seat_class': seat_class,
            'mobile': mobile,
            'email': email,
        }
        # Post booking to booking-service API
        api_url = 'http://localhost:8001/api/bookings/tickets/'
        try:
            resp = requests.post(api_url, json=booking_data)
            if resp.status_code == 201:
                success = 'Booking successful!'
            else:
                error = f"Booking failed: {resp.text}"
        except Exception as e:
            error = str(e)
        return render(request, 'book_flight.html', {'flight': flight, 'error': error, 'success': success})
