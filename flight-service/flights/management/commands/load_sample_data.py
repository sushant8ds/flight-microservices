from django.core.management.base import BaseCommand
from django.utils import timezone
from flights.models import Place, Week, Flight
import csv
import os
from datetime import time, timedelta

class Command(BaseCommand):
    help = 'Load sample flight data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before loading')

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Flight.objects.all().delete()
            Place.objects.all().delete()
            Week.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating days of week...'))
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weeks = {}
        for i, day in enumerate(week_days):
            week, created = Week.objects.get_or_create(
                number=i,
                defaults={'name': day}
            )
            weeks[day] = week
            if created:
                self.stdout.write(f"  ✓ Created {day}")

        # Sample places (top Indian and international airports)
        self.stdout.write(self.style.SUCCESS('Creating places (airports)...'))
        places_data = [
            # India
            {'code': 'DEL', 'city': 'Delhi', 'airport': 'Indira Gandhi International Airport', 'country': 'India'},
            {'code': 'BOM', 'city': 'Mumbai', 'airport': 'Bombay High Airport', 'country': 'India'},
            {'code': 'BLR', 'city': 'Bangalore', 'airport': 'Kempegowda International Airport', 'country': 'India'},
            {'code': 'HYD', 'city': 'Hyderabad', 'airport': 'Rajiv Gandhi International Airport', 'country': 'India'},
            {'code': 'MAA', 'city': 'Chennai', 'airport': 'Chennai International Airport', 'country': 'India'},
            {'code': 'CCU', 'city': 'Kolkata', 'airport': 'Netaji Subhas Chandra Bose International', 'country': 'India'},
            {'code': 'COK', 'city': 'Kochi', 'airport': 'Cochin International Airport', 'country': 'India'},
            {'code': 'PNQ', 'city': 'Pune', 'airport': 'Pune Airport', 'country': 'India'},
            {'code': 'AMD', 'city': 'Ahmedabad', 'airport': 'Sardar Vallabhbhai Patel International', 'country': 'India'},
            {'code': 'JAI', 'city': 'Jaipur', 'airport': 'Jaipur International Airport', 'country': 'India'},
            # International
            {'code': 'LHR', 'city': 'London', 'airport': 'London Heathrow Airport', 'country': 'United Kingdom'},
            {'code': 'CDG', 'city': 'Paris', 'airport': 'Paris Charles de Gaulle Airport', 'country': 'France'},
            {'code': 'AMS', 'city': 'Amsterdam', 'airport': 'Amsterdam Airport Schiphol', 'country': 'Netherlands'},
            {'code': 'DXB', 'city': 'Dubai', 'airport': 'Dubai International Airport', 'country': 'United Arab Emirates'},
            {'code': 'SIN', 'city': 'Singapore', 'airport': 'Singapore Changi Airport', 'country': 'Singapore'},
            {'code': 'HND', 'city': 'Tokyo', 'airport': 'Tokyo Haneda Airport', 'country': 'Japan'},
            {'code': 'PEK', 'city': 'Beijing', 'airport': 'Beijing Capital International Airport', 'country': 'China'},
            {'code': 'LAS', 'city': 'Las Vegas', 'airport': 'Harry Reid International Airport', 'country': 'United States'},
            {'code': 'LAX', 'city': 'Los Angeles', 'airport': 'Los Angeles International Airport', 'country': 'United States'},
            {'code': 'JFK', 'city': 'New York', 'airport': 'John F. Kennedy International Airport', 'country': 'United States'},
        ]

        places = {}
        for place_data in places_data:
            place, created = Place.objects.get_or_create(
                code=place_data['code'],
                defaults={
                    'city': place_data['city'],
                    'airport': place_data['airport'],
                    'country': place_data['country']
                }
            )
            places[place_data['code']] = place
            if created:
                self.stdout.write(f"  ✓ Created {place_data['city']} ({place_data['code']})")

        # Sample flights
        self.stdout.write(self.style.SUCCESS('Creating sample flights...'))
        flights_data = [
            # Domestic flights
            {
                'origin': 'DEL', 'destination': 'BOM', 'plane': 'AI-101', 'airline': 'Air India',
                'depart_time': '06:00', 'arrival_time': '08:30', 'duration': 150,
                'economy_fare': 5000, 'business_fare': 12000, 'first_fare': 18000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            },
            {
                'origin': 'DEL', 'destination': 'BLR', 'plane': 'AI-202', 'airline': 'Air India',
                'depart_time': '10:00', 'arrival_time': '12:30', 'duration': 150,
                'economy_fare': 4500, 'business_fare': 11000, 'first_fare': 16000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            },
            {
                'origin': 'BOM', 'destination': 'BLR', 'plane': 'SG-303', 'airline': 'SpiceJet',
                'depart_time': '14:00', 'arrival_time': '16:15', 'duration': 135,
                'economy_fare': 3500, 'business_fare': 8500, 'first_fare': 12000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            },
            {
                'origin': 'DEL', 'destination': 'HYD', 'plane': 'UK-104', 'airline': 'Vistara',
                'depart_time': '08:30', 'arrival_time': '10:45', 'duration': 135,
                'economy_fare': 4200, 'business_fare': 10500, 'first_fare': 15000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            },
            {
                'origin': 'BOM', 'destination': 'MAA', 'plane': 'AI-305', 'airline': 'Air India',
                'depart_time': '11:00', 'arrival_time': '13:45', 'duration': 165,
                'economy_fare': 4800, 'business_fare': 11500, 'first_fare': 16500,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            },
            {
                'origin': 'BLR', 'destination': 'COK', 'plane': 'SG-406', 'airline': 'SpiceJet',
                'depart_time': '07:30', 'arrival_time': '09:15', 'duration': 105,
                'economy_fare': 2500, 'business_fare': 6000, 'first_fare': 9000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            },
            # International flights
            {
                'origin': 'DEL', 'destination': 'LHR', 'plane': 'AI-191', 'airline': 'Air India',
                'depart_time': '23:30', 'arrival_time': '10:50', 'duration': 510,
                'economy_fare': 35000, 'business_fare': 95000, 'first_fare': 150000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            },
            {
                'origin': 'BOM', 'destination': 'DXB', 'plane': 'EK-501', 'airline': 'Emirates',
                'depart_time': '09:00', 'arrival_time': '12:00', 'duration': 180,
                'economy_fare': 15000, 'business_fare': 45000, 'first_fare': 75000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            },
            {
                'origin': 'DEL', 'destination': 'SIN', 'plane': 'SQ-405', 'airline': 'Singapore Airlines',
                'depart_time': '22:00', 'arrival_time': '05:45', 'duration': 390,
                'economy_fare': 28000, 'business_fare': 80000, 'first_fare': 130000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            },
            {
                'origin': 'BOM', 'destination': 'CDG', 'plane': 'AF-272', 'airline': 'Air France',
                'depart_time': '21:00', 'arrival_time': '08:30', 'duration': 540,
                'economy_fare': 38000, 'business_fare': 110000, 'first_fare': 180000,
                'days': ['Monday', 'Wednesday', 'Friday', 'Saturday']
            },
        ]

        for flight_data in flights_data:
            try:
                origin = places[flight_data['origin']]
                destination = places[flight_data['destination']]
                
                flight, created = Flight.objects.get_or_create(
                    origin=origin,
                    destination=destination,
                    plane=flight_data['plane'],
                    defaults={
                        'airline': flight_data['airline'],
                        'depart_time': time(*map(int, flight_data['depart_time'].split(':'))),
                        'arrival_time': time(*map(int, flight_data['arrival_time'].split(':'))),
                        'duration': timedelta(minutes=flight_data['duration']),
                        'economy_fare': flight_data['economy_fare'],
                        'business_fare': flight_data['business_fare'],
                        'first_fare': flight_data['first_fare'],
                    }
                )
                
                if created:
                    # Add days
                    for day in flight_data['days']:
                        flight.depart_day.add(weeks[day])
                    self.stdout.write(
                        f"  ✓ Created flight {flight_data['origin']}-{flight_data['destination']} "
                        f"({flight_data['plane']})"
                    )
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Error creating flight: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('\n✓ Data loading complete!'))
        self.stdout.write(f"  • Created {len(places)} airports")
        self.stdout.write(f"  • Created {len(week_days)} days of week")
        self.stdout.write(f"  • Created {len(flights_data)} flights")
