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
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            reservation = Reservation.objects.get(pk=pk)
            serializer = ReservationSerializer(reservation)
            if reservation.user.id == request.auth.user.id:
                return Response(serializer.data)
            else:
                return Response({"message": "You cannot view another users reservation"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    
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
    
    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code

        """
        trip_vehicle = TripVehicle.objects.get(pk=request.data['tripVehicleId'])

        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.scheduled_datetime = request.data['scheduled_datetime']
            reservation.trip_vehicle = trip_vehicle

            if reservation.user.id == request.auth.user.id:
                reservation.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You cannot edit another users reservation.'}, status=status.HTTP_403_FORBIDDEN)
            
        except Reservation.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            reservation = Reservation.objects.get(pk=pk)
            if reservation.user.id == request.auth.user.id:
                reservation.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You cannot delete another users reservation.'}, status=status.HTTP_403_FORBIDDEN)

        except Reservation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('id', 'name',)

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ('id', 'name',)
        

class TripVehicleSerializer(serializers.ModelSerializer):

    trip = TripSerializer(many=False)
    vehicle = VehicleSerializer(many=False)

    class Meta:
        model = TripVehicle
        fields = ('id', 'trip', 'vehicle',)



class ReservationSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    trip_vehicle = TripVehicleSerializer(many=False)

    class Meta:
        model = Reservation
        fields = ( 'id', 'user', 'scheduled_datetime', 'trip_vehicle', )

