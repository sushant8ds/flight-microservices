#!/usr/bin/env python
import os
import sys
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_project.settings')
django.setup()

from flights.models import Place, Week, Flight
from datetime import time, timedelta

# Create weeks
print("Creating days of week...")
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weeks = {}
for i, day in enumerate(week_days):
    week, _ = Week.objects.get_or_create(number=i, defaults={'name': day})
    weeks[day] = week
print(f"✓ Created {len(week_days)} days")

# Create places
print("Creating airports...")
places_data = [
    ('DEL', 'Delhi', 'Indira Gandhi International Airport', 'India'),
    ('BOM', 'Mumbai', 'Bombay High Airport', 'India'),
    ('BLR', 'Bangalore', 'Kempegowda International Airport', 'India'),
    ('HYD', 'Hyderabad', 'Rajiv Gandhi International Airport', 'India'),
    ('MAA', 'Chennai', 'Chennai International Airport', 'India'),
    ('CCU', 'Kolkata', 'Netaji Subhas Chandra Bose International', 'India'),
    ('COK', 'Kochi', 'Cochin International Airport', 'India'),
    ('PNQ', 'Pune', 'Pune Airport', 'India'),
    ('AMD', 'Ahmedabad', 'Sardar Vallabhbhai Patel International', 'India'),
    ('JAI', 'Jaipur', 'Jaipur International Airport', 'India'),
    ('LHR', 'London', 'London Heathrow Airport', 'United Kingdom'),
    ('CDG', 'Paris', 'Paris Charles de Gaulle Airport', 'France'),
    ('DXB', 'Dubai', 'Dubai International Airport', 'United Arab Emirates'),
    ('SIN', 'Singapore', 'Singapore Changi Airport', 'Singapore'),
]
places = {}
for code, city, airport, country in places_data:
    place, _ = Place.objects.get_or_create(code=code, defaults={'city': city, 'airport': airport, 'country': country})
    places[code] = place
print(f"✓ Created {len(places_data)} airports")

# Create sample flights
print("Creating sample flights...")
# Clear existing for demo
Flight.objects.all().delete()

flights_to_create = [
    ('DEL', 'BOM', 'AI-101', 'Air India', '06:00', '08:30', 150, 5000, 12000, 18000, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']),
    ('BOM', 'BLR', 'SG-303', 'SpiceJet', '14:00', '16:15', 135, 3500, 8500, 12000, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
    ('DEL', 'HYD', 'UK-104', 'Vistara', '08:30', '10:45', 135, 4200, 10500, 15000, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']),
    ('BOM', 'MAA', 'AI-305', 'Air India', '11:00', '13:45', 165, 4800, 11500, 16500, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
    ('BLR', 'COK', 'SG-406', 'SpiceJet', '07:30', '09:15', 105, 2500, 6000, 9000, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
    ('DEL', 'BLR', 'AI-202', 'Air India', '10:00', '12:30', 150, 4500, 11000, 16000, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
    ('BOM', 'DXB', 'EK-501', 'Emirates', '09:00', '12:00', 180, 15000, 45000, 75000, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
]

count = 0
for origin_code, dest_code, plane, airline, depart, arrival, duration, eco, biz, first_class, days in flights_to_create:
    depart_h, depart_m = map(int, depart.split(':'))
    arrival_h, arrival_m = map(int, arrival.split(':'))
    
    flight, created = Flight.objects.get_or_create(
        origin=places[origin_code],
        destination=places[dest_code],
        plane=plane,
        defaults={
            'airline': airline,
            'depart_time': time(depart_h, depart_m),
            'arrival_time': time(arrival_h, arrival_m),
            'duration': timedelta(minutes=duration),
            'economy_fare': eco,
            'business_fare': biz,
            'first_fare': first_class,
        }
    )
    if created:
        for day in days:
            flight.depart_day.add(weeks[day])
        count += 1
        print(f"  ✓ {origin_code} → {dest_code} ({plane})")

print(f"\n✓ Data loading complete! Created {count} flights")

def get_all_flights():
    """
    Fetch all flights from the flight-service API.
    Returns a list of flight dicts.
    """
    # Change the host/port if running in Docker or production
    FLIGHT_API_URL = "http://localhost:8000/api/flights/flights/"
    try:
        response = requests.get(FLIGHT_API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('flights', [])
    except Exception as e:
        print(f"Error fetching flights: {e}")
        return []

# Example usage:
if __name__ == "__main__":
    flights = get_all_flights()
    print(f"Fetched {len(flights)} flights.")
    if flights:
        print(flights[0])  # Print first flight as example
