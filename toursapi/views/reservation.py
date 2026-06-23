from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from toursapi.models import Reservation, TripVehicle, Trip, Vehicle


class ReservationView(ViewSet):
    """Void view set"""

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            reservations = Reservation.objects.filter(user=request.auth.user)
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        """Handle POST requests for Reservations

        Returns:
            Response: JSON serialized representation of newly created Reservation
        """
        # TODO: Wrap this in a try/except block to handle errors/bad requests and send back appropriate messages and codes.

        # Get an object instance of a trip_vehicle type
        trip_vehicle = TripVehicle.objects.get(pk=request.data['tripVehicleId'])

        # Create a reservation object and assign it property values
        reservation = Reservation()
        reservation.user = request.auth.user
        reservation.scheduled_datetime = request.data['scheduled_datetime']
        reservation.trip_vehicle = trip_vehicle
        reservation.save()

        serialized = ReservationSerializer(reservation, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('name',)

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ('name',)
        

class TripVehicleSerializer(serializers.ModelSerializer):

    trip = TripSerializer(many=False)
    vehicle = VehicleSerializer(many=False)

    class Meta:
        model = TripVehicle
        fields = ('trip', 'vehicle',)



class ReservationSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    trip_vehicle = TripVehicleSerializer(many=False)

    class Meta:
        model = Reservation
        fields = ( 'id', 'user', 'scheduled_datetime', 'trip_vehicle', )

