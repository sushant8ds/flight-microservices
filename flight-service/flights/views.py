from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Flight, Place, Week, Passenger
from .serializers import (
    FlightListSerializer, FlightDetailSerializer, 
    FlightCreateSerializer, PlaceSerializer, WeekSerializer,
    PassengerSerializer
)


class FlightViewSet(viewsets.ModelViewSet):
    """ViewSet for Flight operations"""
    queryset = Flight.objects.all()
    permission_classes = []

    def get_permissions(self):
        # Allow unauthenticated access to list (GET) endpoint
        if self.action == 'list':
            return []
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return FlightCreateSerializer
        elif self.action == 'retrieve':
            return FlightDetailSerializer
        return FlightListSerializer

    def list(self, request, *args, **kwargs):
        """List all flights"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "flights": serializer.data,
                "total": queryset.count()
            })
        except Exception as e:
            import traceback
            print('FLIGHT API ERROR:', e)
            traceback.print_exc()
            return Response({"error": str(e), "trace": traceback.format_exc()}, status=500)

    def create(self, request, *args, **kwargs):
        """Create a new flight (authenticated users only)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """Get flight details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet for Place operations"""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """List all airports/places"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "places": serializer.data,
            "total": queryset.count()
        })


class WeekViewSet(viewsets.ModelViewSet):
    """ViewSet for Week operations"""
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    permission_classes = [IsAuthenticated]


class PassengerViewSet(viewsets.ModelViewSet):
    """ViewSet for Passenger operations"""
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]

