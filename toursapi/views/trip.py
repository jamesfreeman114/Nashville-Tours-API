from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from toursapi.models import Trip

class TripView(ViewSet):
    
    def list(self, request):
        """Handle GET requests for all trips

        Returns:
            Response -- JSON serialized array
        """
        try:
            trips = Trip.objects.all()
            serializer = TripSerializer(trips, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('id', 'name', 'description', 'image_path')

