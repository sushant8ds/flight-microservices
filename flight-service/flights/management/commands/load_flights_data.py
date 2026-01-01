from django.core.management.base import BaseCommand
from flights.utils import (
    createWeekDays,
    addPlaces,
    cleanDuplicatePlaces,
    addDomesticFlights,
    addInternationalFlights
)


class Command(BaseCommand):
    help = 'Load complete flight data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before loading')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data load...\n'))
        
        try:
            createWeekDays()
            addPlaces()
            cleanDuplicatePlaces()
            addDomesticFlights()
            addInternationalFlights()
            
            self.stdout.write(self.style.SUCCESS('\n✓ All data loaded successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
