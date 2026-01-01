from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time, timedelta
from flights.models import Place, Week, Flight


class Command(BaseCommand):
    help = 'Populate sample flight data'

    def handle(self, *args, **options):
        self.stdout.write('Creating places...')
        
        # Create places
        places = {
            'delhi': Place.objects.get_or_create(
                code='DEL',
                defaults={'city': 'Delhi', 'airport': 'Indira Gandhi', 'country': 'India'}
            )[0],
            'mumbai': Place.objects.get_or_create(
                code='BOM',
                defaults={'city': 'Mumbai', 'airport': 'Bombay High', 'country': 'India'}
            )[0],
            'bangalore': Place.objects.get_or_create(
                code='BLR',
                defaults={'city': 'Bangalore', 'airport': 'Kempegowda', 'country': 'India'}
            )[0],
            'chennai': Place.objects.get_or_create(
                code='MAA',
                defaults={'city': 'Chennai', 'airport': 'Chennai International', 'country': 'India'}
            )[0],
            'kolkata': Place.objects.get_or_create(
                code='CCU',
                defaults={'city': 'Kolkata', 'airport': 'Netaji Subhas Chandra Bose', 'country': 'India'}
            )[0],
        }
        
        self.stdout.write('Creating weeks...')
        
        # Create weeks
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weeks = {}
        for i, day in enumerate(week_days):
            week, _ = Week.objects.get_or_create(
                number=i,
                defaults={'name': day}
            )
            weeks[day] = week
        
        self.stdout.write('Creating flights...')
        
        # Create flights
        flights_data = [
            {
                'origin': places['delhi'],
                'destination': places['mumbai'],
                'airline': 'Air India',
                'plane': 'AI101',
                'depart_time': time(10, 0),
                'arrival_time': time(12, 30),
                'economy_fare': 5000,
                'business_fare': 8000,
                'first_fare': 12000,
                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            },
            {
                'origin': places['mumbai'],
                'destination': places['bangalore'],
                'airline': 'IndiGo',
                'plane': '6E202',
                'depart_time': time(14, 0),
                'arrival_time': time(16, 15),
                'economy_fare': 4500,
                'business_fare': 7500,
                'first_fare': 11000,
                'days': ['Monday', 'Wednesday', 'Friday', 'Saturday', 'Sunday']
            },
            {
                'origin': places['bangalore'],
                'destination': places['delhi'],
                'airline': 'Vistara',
                'plane': 'UK825',
                'depart_time': time(11, 0),
                'arrival_time': time(13, 45),
                'economy_fare': 4800,
                'business_fare': 8200,
                'first_fare': 12500,
                'days': ['Tuesday', 'Thursday', 'Saturday']
            },
            {
                'origin': places['delhi'],
                'destination': places['chennai'],
                'airline': 'Air India Express',
                'plane': 'IX301',
                'depart_time': time(8, 30),
                'arrival_time': time(11, 45),
                'economy_fare': 5500,
                'business_fare': 9000,
                'first_fare': 13000,
                'days': ['Daily', 'Daily', 'Daily', 'Daily', 'Daily', 'Daily', 'Daily']
            },
            {
                'origin': places['kolkata'],
                'destination': places['mumbai'],
                'airline': 'GoAir',
                'plane': 'G8402',
                'depart_time': time(15, 30),
                'arrival_time': time(18, 00),
                'economy_fare': 6000,
                'business_fare': 9500,
                'first_fare': 14000,
                'days': ['Wednesday', 'Friday', 'Sunday']
            },
        ]
        
        for flight_data in flights_data:
            days = flight_data.pop('days')
            flight, created = Flight.objects.get_or_create(
                airline=flight_data['airline'],
                plane=flight_data['plane'],
                defaults=flight_data
            )
            
            # Add departure days
            for day_name in days:
                if day_name != 'Daily':
                    flight.depart_day.add(weeks[day_name])
                else:
                    # Add all days
                    flight.depart_day.set(list(weeks.values()))
                    break
            
            if created:
                self.stdout.write(f"  ✓ Created {flight_data['airline']} {flight_data['plane']}")
            else:
                self.stdout.write(f"  → {flight_data['airline']} {flight_data['plane']} already exists")
        
        self.stdout.write(self.style.SUCCESS('✓ Sample data populated successfully!'))
