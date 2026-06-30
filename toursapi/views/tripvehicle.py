from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..models import Vehicle, Trip, TripVehicle

class TripVehicleView(ViewSet):

    def list(self, request):

        trip_option = self.request.query_params.get('trip', None)
        
        try:
            trip_vehicles = TripVehicle.objects.all()

            if trip_option is not None: 
                trip_vehicles = TripVehicle.objects.filter(trip=trip_option)

            serializer = TripVehicleSerializer(trip_vehicles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
    


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('name',)

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ('name',)


class TripVehicleSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    trip = TripSerializer(many=False)
    vehicle = VehicleSerializer(many=False)

    class Meta:
        model = TripVehicle
        fields = ( 'id', 'trip', 'vehicle', )



