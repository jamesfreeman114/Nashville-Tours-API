from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from toursapi.models import Review, Trip

class ReviewView(ViewSet):

    def list(self, request):

        trip = self.request.query_params.get('trip', None)
        reviewer_only = self.request.query_params.get('reviewer', None)

        try:
            reviews = Review.objects.all()

            if trip is not None:
                reviews = Review.objects.filter(trip=trip)

            if reviewer_only is not None and reviewer_only == "current":
                reviews = Review.objects.filter(user=request.auth.user) 

            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def retrieve(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)

            if review.user.id == request.auth.user.id:
                return Response(serializer.data)
            else:
                return Response({"message": "You do not have access to this review"}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):

        trip = Trip.objects.get(pk=request.data['tripId'])

        review = Review()
        review.user = request.auth.user
        review.rating = request.data['rating']
        review.comment = request.data['comment']
        review.trip = trip
        review.save()

        serialized = ReviewSerializer(review, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
            review.rating = request.data['rating']
            review.comment = request.data['comment']

            if review.user.id == request.auth.user.id:
                review.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You cannot change another user's review"}, status=status.HTTP_403_FORBIDDEN)
        
        except Review.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
            if review.user.id == request.auth.user.id:
                review.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You cannot delete another user's review."}, status=status.HTTP_403_FORBIDDEN)
        
        except Review.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('id', 'name',)
        
class ReviewSerializer(serializers.ModelSerializer):

    trip = TripSerializer(many=False)
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'trip', 'rating', 'comment')

    