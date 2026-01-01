from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer, TicketCreateSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """ViewSet for Ticket/Booking operations"""
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer
    
    def get_queryset(self):
        """Return bookings for current user only"""
        return Ticket.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """List all bookings for current user"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "bookings": serializer.data,
            "total": queryset.count()
        })
    
    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(TicketSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """Get booking details"""
        instance = self.get_object()
        serializer = TicketSerializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        ticket = self.get_object()
        if ticket.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if ticket.status == 'cancelled':
            return Response({'error': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        
        ticket.status = 'cancelled'
        ticket.save()
        return Response(TicketSerializer(ticket).data)

