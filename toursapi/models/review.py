from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name="trip")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length=280)
