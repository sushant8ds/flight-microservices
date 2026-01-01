import csv
from django.core.management.base import BaseCommand
from flights.models import Flight, Airport
from django.utils import timezone

class Command(BaseCommand):
    help = 'Import flights from domestic_flights.csv'

    def handle(self, *args, **options):
        path = 'Data/domestic_flights.csv'
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    origin_code = row['origin']
                    dest_code = row['destination']
                    origin = Airport.objects.filter(code=origin_code).first()
                    destination = Airport.objects.filter(code=dest_code).first()
                    if not origin or not destination:
                        continue
                    flight = Flight(
                        origin=origin,
                        destination=destination,
                        depart_time=row['depart_time'],
                        arrival_time=row['arrival_time'],
                        airline=row['airline'],
                        plane=row['flight_no'],
                        economy_fare=row['economy_fare'] or 0,
                        business_fare=row['business_fare'] or 0,
                        first_fare=row['first_fare'] or 0,
                        duration=row['duration'],
                    )
                    flight.save()
                    count += 1
                except Exception as e:
                    print(f'Error: {e}')
        print(f'Imported {count} flights.')
