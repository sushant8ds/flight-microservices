from rest_framework import serializers
from .models import Place, Week, Flight, Passenger


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'city', 'airport', 'code', 'country']


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['id', 'number', 'name']


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'first_name', 'last_name', 'gender']


class FlightListSerializer(serializers.ModelSerializer):
    origin = PlaceSerializer(read_only=True)
    destination = PlaceSerializer(read_only=True)
    depart_day = WeekSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = ['id', 'origin', 'destination', 'depart_time', 'arrival_time', 
                  'airline', 'plane', 'economy_fare', 'business_fare', 'first_fare', 
                  'depart_day']


class FlightDetailSerializer(serializers.ModelSerializer):
    origin = PlaceSerializer(read_only=True)
    destination = PlaceSerializer(read_only=True)
    depart_day = WeekSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = ['id', 'origin', 'destination', 'depart_time', 'arrival_time', 
                  'duration', 'airline', 'plane', 'economy_fare', 'business_fare', 
                  'first_fare', 'depart_day']


class FlightCreateSerializer(serializers.ModelSerializer):
    depart_day = serializers.PrimaryKeyRelatedField(
        queryset=Week.objects.all(), many=True
    )
    
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'depart_time', 'arrival_time', 'duration',
                  'plane', 'airline', 'economy_fare', 'business_fare', 'first_fare', 
                  'depart_day']
    
    def create(self, validated_data):
        depart_days = validated_data.pop('depart_day', [])
        flight = Flight.objects.create(**validated_data)
        flight.depart_day.set(depart_days)
        return flight
