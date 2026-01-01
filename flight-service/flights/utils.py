from datetime import datetime, timedelta
from django.db.models import Count
from flights.models import Week, Place, Flight
import os

def get_number_of_lines(file):
    """Count lines in a file"""
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def createWeekDays():
    """Create week days in database"""
    print("Creating week days...")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    count = 0
    for i, day in enumerate(days):
        week, created = Week.objects.get_or_create(number=i, defaults={"name": day})
        if created:
            count += 1
    print(f"✓ Created {count} week days")


def addPlaces():
    """Add airports from CSV file"""
    print("Adding Airports from CSV...")
    
    # Get the directory where this file is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), 'Data')
    csv_file = os.path.join(data_dir, 'airports.csv')
    
    if not os.path.exists(csv_file):
        print(f"✗ CSV file not found: {csv_file}")
        return
    
    total = get_number_of_lines(csv_file)
    count = 0
    
    with open(csv_file) as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            
            try:
                parts = [x.strip() for x in line.split(",")]
                if len(parts) < 4:
                    continue
                    
                city, airport, code, country = parts[0], parts[1], parts[2], parts[3]

                # Avoid duplicates
                if Place.objects.filter(code=code).exists():
                    continue

                Place.objects.create(
                    city=city,
                    airport=airport,
                    code=code,
                    country=country,
                )
                count += 1
                
                if count % 100 == 0:
                    print(f"  ... loaded {count} airports")
                    
            except Exception as e:
                print(f"  Error on line {i}: {e}")
                continue
    
    print(f"✓ Added {count} airports")


def cleanDuplicatePlaces():
    """Remove duplicate airport entries from DB"""
    print("Cleaning duplicate airports...")
    
    duplicates = (
        Place.objects.values("code")
        .annotate(c=Count("code"))
        .filter(c__gt=1)
    )

    count = 0
    for dup in duplicates:
        code = dup["code"]
        places = Place.objects.filter(code=code)
        # keep first, delete others
        deleted = places.exclude(id=places.first().id).delete()
        count += deleted[0]
    
    print(f"✓ Cleaned {count} duplicate airports")


def addDomesticFlights():
    """Add domestic flights from CSV file"""
    print("Adding Domestic Flights...")
    
    # Get the directory where this file is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), 'Data')
    csv_file = os.path.join(data_dir, 'domestic_flights.csv')
    
    if not os.path.exists(csv_file):
        print(f"✗ CSV file not found: {csv_file}")
        return
    
    total = get_number_of_lines(csv_file)
    count = 0
    errors = 0
    
    with open(csv_file) as file:
        for i, line in enumerate(file):
            if i == 0:
                continue

            try:
                data = [x.strip() for x in line.split(",")]
                if len(data) < 14:
                    continue

                origin = data[1]
                destination = data[2]
                depart_time = datetime.strptime(data[3], "%H:%M:%S").time()
                week_no = int(data[4])
                duration = timedelta(hours=int(data[5][:2]), minutes=int(data[5][3:5]))
                arrive_time = datetime.strptime(data[6], "%H:%M:%S").time()
                flight_no = data[8]
                airline = data[10]
                eco = float(data[11] or 0)
                bus = float(data[12] or 0)
                fst = float(data[13] or 0)

                origin_place = Place.objects.filter(code=origin).first()
                dest_place = Place.objects.filter(code=destination).first()
                
                if not origin_place or not dest_place:
                    continue

                flight = Flight.objects.create(
                    origin=origin_place,
                    destination=dest_place,
                    depart_time=depart_time,
                    duration=duration,
                    arrival_time=arrive_time,
                    plane=flight_no,
                    airline=airline,
                    economy_fare=eco,
                    business_fare=bus,
                    first_fare=fst,
                )
                
                week = Week.objects.filter(number=week_no).first()
                if week:
                    flight.depart_day.add(week)
                    flight.save()
                    count += 1
                
                if count % 100 == 0:
                    print(f"  ... loaded {count} flights")

            except Exception as e:
                errors += 1
                if errors <= 5:  # Only print first 5 errors
                    print(f"  Error on line {i}: {e}")
                continue

    print(f"✓ Added {count} domestic flights")


def addInternationalFlights():
    """Add international flights from CSV file"""
    print("Adding International Flights...")
    
    # Get the directory where this file is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), 'Data')
    csv_file = os.path.join(data_dir, 'international_flights.csv')
    
    if not os.path.exists(csv_file):
        print(f"✗ CSV file not found: {csv_file}")
        return
    
    total = get_number_of_lines(csv_file)
    count = 0
    errors = 0
    
    with open(csv_file) as file:
        for i, line in enumerate(file):
            if i == 0:
                continue

            try:
                data = [x.strip() for x in line.split(",")]
                if len(data) < 14:
                    continue

                origin = data[1]
                destination = data[2]
                depart_time = datetime.strptime(data[3], "%H:%M:%S").time()
                week_no = int(data[4])
                duration = timedelta(hours=int(data[5][:2]), minutes=int(data[5][3:5]))
                arrive_time = datetime.strptime(data[6], "%H:%M:%S").time()
                flight_no = data[8]
                airline = data[10]
                eco = float(data[11] or 0)
                bus = float(data[12] or 0)
                fst = float(data[13] or 0)

                origin_place = Place.objects.filter(code=origin).first()
                dest_place = Place.objects.filter(code=destination).first()
                
                if not origin_place or not dest_place:
                    continue

                flight = Flight.objects.create(
                    origin=origin_place,
                    destination=dest_place,
                    depart_time=depart_time,
                    duration=duration,
                    arrival_time=arrive_time,
                    plane=flight_no,
                    airline=airline,
                    economy_fare=eco,
                    business_fare=bus,
                    first_fare=fst,
                )
                
                week = Week.objects.filter(number=week_no).first()
                if week:
                    flight.depart_day.add(week)
                    flight.save()
                    count += 1
                
                if count % 100 == 0:
                    print(f"  ... loaded {count} flights")

            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  Error on line {i}: {e}")
                continue

    print(f"✓ Added {count} international flights")
