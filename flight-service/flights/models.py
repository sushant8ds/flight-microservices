from django.db import models

class Place(models.Model):
    """Airports and locations"""
    city = models.CharField(max_length=64)
    airport = models.CharField(max_length=64)
    code = models.CharField(max_length=3)  # Airport code
    country = models.CharField(max_length=64)

    class Meta:
        db_table = 'flight_place'
    
    def __str__(self):
        return f"{self.city} ({self.code})"


class Week(models.Model):
    """Days of the week"""
    number = models.IntegerField()  # 0-6
    name = models.CharField(max_length=16)

    class Meta:
        db_table = 'flight_week'
    
    def __str__(self):
        return self.name


class Flight(models.Model):
    """Flight model"""
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='arrivals')
    depart_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.DurationField(null=True, blank=True)
    plane = models.CharField(max_length=24)  # Flight number
    airline = models.CharField(max_length=64)
    
    # Fares for different classes
    economy_fare = models.FloatField(null=True, blank=True)
    business_fare = models.FloatField(null=True, blank=True)
    first_fare = models.FloatField(null=True, blank=True)
    
    # Days the flight operates
    depart_day = models.ManyToManyField(Week, related_name='flights_of_the_day')

    class Meta:
        db_table = 'flight_flight'
    
    def __str__(self):
        return f"{self.airline} {self.plane} ({self.origin} -> {self.destination})"


class Passenger(models.Model):
    """Passenger model"""
    GENDER_CHOICES = [('male', 'MALE'), ('female', 'FEMALE')]
    
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)

    class Meta:
        db_table = 'flight_passenger'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
