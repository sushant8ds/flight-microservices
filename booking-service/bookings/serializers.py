from rest_framework import serializers
from .models import Ticket
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'ref_no', 'flight_id', 'passenger_names', 
                  'flight_ddate', 'flight_adate', 'flight_fare', 'other_charges',
                  'coupon_used', 'coupon_discount', 'total_fare', 'seat_class', 
                  'mobile', 'email', 'status', 'booking_date']
        read_only_fields = ['id', 'user', 'booking_date']


class TicketCreateSerializer(serializers.ModelSerializer):
    passenger_names = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of passenger names"
    )
    
    class Meta:
        model = Ticket
        fields = ['ref_no', 'flight_id', 'passenger_names', 'flight_ddate', 
                  'flight_adate', 'flight_fare', 'other_charges', 'coupon_used',
                  'coupon_discount', 'total_fare', 'seat_class', 'mobile', 'email']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Ticket.objects.create(**validated_data)
