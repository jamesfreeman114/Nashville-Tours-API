from django.db import models
from .review import Review

class Trip(models.Model):
    name = models.CharField(max_length=155)
    description = models.CharField(max_length=600)
    image_path = models.CharField(max_length=200)

    @property
    def average_rating(self):

        result = Review.objects.filter(trip=self).aggregate(
            models.Avg("rating")
        )
        return result["rating__avg"] or 0
    
