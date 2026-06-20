from django.db import models
from django.contrib.auth.models import User
from .trip_vehicle import TripVehicle

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    trip_vehicle = models.ForeignKey(TripVehicle, on_delete=models.CASCADE)
